import psycopg
from typing import Any

def is_int(s: str):
    try:
        int(s)
        return True
    except:
        return False

def rate(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) < 2 or not is_int(args[-1]):
        print(
            "Usage: rate [title] [rating: 0-5]")
        return

    if 'uid' not in ctx:
        print("Not logged in. Please use the log in command to continuing!")
        return
    uid = int(ctx['uid'])


    title = " ".join(args[0:-1])
    rating = args[-1]
    if int(rating) not in range(1, 6):
        print(
            "Usage: rating must be a integer from 1 to 5")
        return

    with conn.cursor() as cur:
        try:

            cur.execute("""
                INSERT INTO user_rating (uid,vid,rating)
                VALUES (%s,(SELECT vid FROM video_games WHERE title = %s),%s)
                ON CONFLICT (uid, vid) DO UPDATE SET rating = EXCLUDED.rating;
            """, (uid, title, rating)
            )
            conn.commit()
        except psycopg.errors.NotNullViolation:
            print(f"failed: could not find video game named '{title}'")
            return

        print(f"Successfully set rating of '{title}' to {rating}")
