import psycopg
from typing import Any


def rate(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if 'uid' not in ctx:
        print("Not logged in. Please use the log in command to continuing!")
        return

    uid = int(ctx['uid'])

    if len(args) != 2:
        print(
            "Usage: rate [title] [rating]\n rating must be a integer from 1 to 5")
        return

    title = args[0]
    rating = int(args[1])
    print(type(rating),  rating > 0, rating < 6)
    if rating < 0 or rating > 6:
        print(
            "Usage: rating must be a integer from 1 to 5")
        return

    try:
        with conn.cursor() as cur:
            # Random Game Query
            cur.execute("""
                SELECT vid
                FROM video_games
                WHERE title = %s
            """, (title,))
            vid = cur.fetchone()[0]
            cur.execute("""
                SELECT rating
                FROM user_rating
                WHERE uid = %s AND vid = %s
            """, (uid, vid)
            )
            ver = cur.fetchone()
            print(ver)
            if (ver is None):
                cur.execute("""
                    INSERT INTO user_rating (uid,vid,rating) VALUES (%s,%s,%s)
                """, (uid, vid, str(rating)))
                print(f"Successfully Rated {title}, '{rating}'")
            else:
                print("updating")
                cur.execute("""
                    UPDATE user_rating
                    SET rating = %s
                    WHERE uid = %s AND vid = %s
                """, (str(rating), uid, vid)
                )
                print(f"Updated rating of {title} to '{rating}'")
            conn.commit()
    except Exception as error:
        print(f"Exception: {error}")
        return
