import psycopg
from typing import Any
from datetime import date, timedelta
import calendar

def top_20_rolling(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if (len(args) != 0):
        print("usage: top_20_rolling")
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
                AND end_time <= %s
                AND up.vid = vg.vid
            GROUP BY
                up.vid, vg.title, vg.vid
            ORDER BY
                total DESC''', (date.today() - timedelta(days=90), date.today()))
        
        result = cur.fetchall()
        print("Top "+ str(min(len(result), 20)) +" Games of the Last 90 Days:")
        print("---------------------------------")
        for i in range(20):
            if(len(result) == i): break
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
    
    today = date.today()
    with conn.cursor() as cur:
        cur.execute('''
            SELECT
                up.vid,
                vg.vid,
                vg.title,
                up.end_time,
                up.start_time,
                SUM(end_time - start_time) AS total
            FROM
                user_plays AS up,
                video_games AS vg
            WHERE
                up.vid = vg.vid
                AND 
                ((start_time >= %s AND start_time <= %s) OR (end_time >= %s AND end_time <= %s))
            GROUP BY
                up.vid, vg.title, vg.vid, up.end_time, up.start_time
            ORDER BY
                total DESC''', (today.replace(day=1), 
                                today.replace(day=calendar.monthrange(today.year, today.month)[1]),
                                today.replace(day=1), 
                                today.replace(day=calendar.monthrange(today.year, today.month)[1])))
        
        result = cur.fetchall()
        print(calendar.month_name[date.today().month] + "'s Top " + str(min(len(result), 5)) + " Games:")
        print("----------------------")
        for i in range(5):
            if(len(result) == i): break
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
            WHERE up.uid = 1922
            GROUP BY v.title, v.vid
            ORDER BY total DESC)
        SELECT
            tp.title,
            STRING_AGG(DISTINCT g.genre, ', ') as genres,
            STRING_AGG(DISTINCT dev.name, ', ') as developers,
            STRING_AGG(DISTINCT pub.name, ', ') as publishers
        FROM total_playtime tp
        LEFT JOIN video_game_genre vgg on vgg.vid = tp.vid
        LEFT JOIN genre g on g.gid = vgg.gid
        LEFT JOIN video_game_developer vgd on vgd.vid = tp.vid
        LEFT JOIN contributor dev on dev.dpid = vgd.dpid
        LEFT JOIN video_game_publisher vgpub on vgpub.vid = tp.vid
        LEFT JOIN contributor pub on pub.dpid = vgpub.dpid
        GROUP BY tp.title, tp.vid, tp.total
        ORDER BY tp.total DESC;''')

        # print(f"Fetchone: {cur.fetchone()}\n\n")
        # print(f"Fetchall: {cur.fetchall()}\n\n")

        for row in cur.fetchall():
            row.index()
        # genre = cur.fetchone()[1].split(', ')
        # print(f"Genre: {genre}")
        # devs = cur.fetchone()[2].split(', ')
        # print(f"Developers: {devs}")
        # pubs = cur.fetchone()[3].split(', ')
        # print(f"Publishers: {pubs}")

