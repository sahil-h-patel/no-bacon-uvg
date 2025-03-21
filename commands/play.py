import psycopg
from typing import Any


def play(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(f"args: {args}")
    print(f"ctx: {ctx}")

    if len(args) == 2:
        title = args[0]
        minutes = int(args[1])
    elif len(args) == 1 and args[0].isdigit():
        minutes = int(args[0])
        title = None
    else:
        print("Usage: play [optional: title] [minutes]")
        return

    uid = ctx['uid']

    if title is not None:
        with conn.cursor() as cur:
            select_game_query = ("""
                SELECT vid
                FROM video_games as v
                WHERE v.title = '%s'
                """ % (title))
            query = (
                """
                    INSERT INTO user_plays (uid,vid,start,end_time)
                    VALUES ('%s', (%s) ,CURRENT_TIMESTAMP, (SELECT CURRENT_TIMESTAMP + INTERVAL '%s minutes'))
                """ % (uid, select_game_query, minutes)
            )
            try:
                cur.execute(query)
                conn.commit()
                print(f"Successfully recorded {
                    minutes} minute(s) of playtime on {title}")
            except Exception as error:
                print(f"Exception: {error}")
    else:
        with conn.cursor() as cur:
            random_game_query = ("""
                SELECT c.vid, v.title
                FROM user_has_collection u, collection_has_video_game c, video_games v
                WHERE u.cid = c.cid AND u.uid = %s AND v.vid = c.vid
                ORDER BY RANDOM()
                LIMIT 1
            """ % (uid))

            cur.execute(random_game_query)
            vid, title = cur.fetchall()[0]

            query = (
                """
                    INSERT INTO user_plays (uid,vid,start,end_time)
                    VALUES ('%s', %s ,CURRENT_TIMESTAMP, (SELECT CURRENT_TIMESTAMP + INTERVAL '%s minutes'))


                """ % (uid, vid, minutes)
            )
            try:
                cur.execute(query)
                conn.commit()
                print(f"Successfully recorded {
                      minutes} minute(s) of playtime on random game: {title}")
            except Exception as error:
                print(f"Exception: {error}")
