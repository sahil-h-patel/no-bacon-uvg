import psycopg
from typing import Any
from datetime import date, timedelta
import calendar

def top_20_rolling(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if (len(args) != 0):
        print("usage: top_20_rolling")
        return
    print(date.today() - timedelta(days=90))

    with conn.cursor() as cur:
        cur.execute('''
            SELECT
                up.vid,
                vg.vid,
                vg.title,
                SUM(end_time - start_time) AS total
            FROM
                user_plays AS up,
                video_games AS vg
            WHERE
                start_time > %s
                AND up.vid = vg.vid
            GROUP BY
                up.vid, vg.title, vg.vid
            ORDER BY
                total DESC''', (date.today() - timedelta(days=90),))
        
        print("Top 20 Games of the Last 90 Days:")
        print("---------------------------------")
        result = cur.fetchall()
        for i in range(20):
            print(str(i+1) + ":\t" + result[i][2])

def top_20_followers(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if(len(args) != 0):
        print("usage: top_20_followers")
        return

    with conn.cursor() as cur:
        cur.execute('''
            SELECT
                vg.vid,
                vg.title,
                SUM(up.end_time - up.start_time) AS total
            FROM users u
            JOIN follows f ON f.follower_uid = u.uid
            JOIN user_plays up ON up.uid = f.followee_uid
            JOIN video_games vg ON up.vid = vg.vid
            WHERE u.uid = %s
            GROUP BY vg.vid, vg.title
            ORDER BY total DESC;''', (ctx['uid'],))
        
        print("Top 20 Games Among My Followers:")
        print("---------------------------------")
        result = cur.fetchall()
        for i in range(20):
            print(str(i+1) + ":\t" + result[i][1])

def top_5_releases_month(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if (len(args) != 0):
        print("usage: top_5_monthly")
        return

    with conn.cursor() as cur:
        cur.execute('''
            SELECT
                up.vid,
                vg.vid,
                vg.title,
                SUM(end_time - start_time) AS total
            FROM
                user_plays AS up,
                video_games AS vg
            WHERE
                start_time > %s
                AND up.vid = vg.vid
            GROUP BY
                up.vid, vg.title, vg.vid
            ORDER BY
                total DESC''', (date.today().replace(day=1) - timedelta(days=30),))
        
        print(calendar.month_name[date.today().month] + "'s Top 5 Games:")
        print("----------------------")
        result = cur.fetchall()
        for i in range(5):
            print(str(i+1) + ":\t" + result[i][2])

def for_you(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if(len(args) != 0):
        print("usage: for_you")
        return
    
    with conn.cursor() as cur:
        cur.execute('''
            WITH total_playtime AS (
                SELECT v.vid, v.title, SUM(up.end_time - up.start_time) as total
                FROM user_plays up
                JOIN video_games v on up.vid = v.vid
                WHERE up.uid = %s
                GROUP BY v.title, v.vid
                ORDER BY total DESC),
            avg_rating AS (
                SELECT
                    ur.vid,
                    AVG(ur.rating) as average_rating
                FROM user_rating ur
                GROUP BY ur.vid
            )
            SELECT
                tp.title,
                STRING_AGG(DISTINCT g.genre, ', ') as genres,
                STRING_AGG(DISTINCT dev.name, ', ') as developers,
                STRING_AGG(DISTINCT pub.name, ', ') as publishers,
                STRING_AGG(DISTINCT p.name, ', ') as platforms,
                ar.average_rating
            FROM total_playtime tp
            LEFT JOIN video_game_genre vgg on vgg.vid = tp.vid
            LEFT JOIN genre g on g.gid = vgg.gid
            LEFT JOIN video_game_developer vgd on vgd.vid = tp.vid
            LEFT JOIN contributor dev on dev.dpid = vgd.dpid
            LEFT JOIN video_game_publisher vgpub on vgpub.vid = tp.vid
            LEFT JOIN contributor pub on pub.dpid = vgpub.dpid
            LEFT JOIN video_game_platforms vgp on vgp.vid = tp.vid
            LEFT JOIN platform p on p.pid = vgp.pid
            LEFT JOIN avg_rating ar on ar.vid = tp.vid
            GROUP BY tp.title, tp.vid, tp.total, ar.average_rating
            ORDER BY tp.total DESC;''', (ctx['uid'],))

        def parse_to_list(s):
            if not s:
                return ["none"]
            # Convert to list if it's not already
            return list(x.strip() for x in s.split(', '))
        
        user_games = cur.fetchall()
        for game in user_games:
            title, genres, developers, publishers, platforms, rating = game
            genre_list = parse_to_list(genres)
            dev_list = parse_to_list(developers)
            pub_list = parse_to_list(publishers)
            plat_list = parse_to_list(platforms)

            if all(x == ["none"] for x in [genre_list, dev_list, pub_list, plat_list]):
                continue  # skip if this game doesn't have enough metadata

            cur.execute('''
                SELECT DISTINCT vg.title, AVG(ur.rating) AS average_rating
                    FROM video_games vg
                    LEFT JOIN video_game_genre vgg ON vg.vid = vgg.vid
                    LEFT JOIN genre g ON g.gid = vgg.gid
                    LEFT JOIN video_game_developer vgd ON vgd.vid = vg.vid
                    LEFT JOIN contributor dev ON dev.dpid = vgd.dpid
                    LEFT JOIN video_game_publisher vgpub ON vgpub.vid = vg.vid
                    LEFT JOIN contributor pub ON pub.dpid = vgpub.dpid
                    LEFT JOIN video_game_platforms vgp ON vgp.vid = vg.vid
                    LEFT JOIN platform p ON p.pid = vgp.pid
                    LEFT JOIN user_rating ur ON ur.vid = vg.vid
                    WHERE vg.vid NOT IN (
                        SELECT DISTINCT vid FROM user_plays WHERE uid = %s
                    )
                    AND (
                        g.genre = ANY(%s) OR
                        dev.name = ANY(%s) OR
                        pub.name = ANY(%s) OR
                        p.name = ANY(%s)
                    )
                    GROUP BY vg.vid, vg.title
                    HAVING AVG(ur.rating) >= %s
                    ORDER BY average_rating DESC
                    LIMIT 5;''', (ctx['uid'], 
                                  genre_list, 
                                  dev_list,
                                  pub_list,
                                  plat_list,
                                  rating))
            result = cur.fetchall()
            for i in range(min(len(result), 5)):  # Avoid index error if less than 5 results
                rating_display = f"(avg rating {result[i][1]:.2f})" if result[i][1] is not None else "(no ratings)"
                print(f"Recommended based on '{title}': {result[i][0]} {rating_display}")