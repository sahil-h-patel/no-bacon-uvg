import psycopg
from datetime import date, datetime, timedelta
from typing import Any

DATE_FORMAT = "%m-%d-%Y"

def _play(conn: psycopg.Connection, uid: Any, title: str, start_time: datetime, playtime: int):
    with conn.cursor() as cur:
        try:
            cur.execute('''
                INSERT INTO user_plays (uid,vid,start_time,end_time)
                VALUES (
                    %s,
                    (SELECT vid FROM video_games WHERE title = %s),
                    %s,
                    %s
                )
            ''', (uid, title, start_time, start_time + timedelta(minutes=playtime)))
        except psycopg.errors.NotNullViolation:
            print(f"failed: could not find video game named '{title}'")
            return
    conn.commit()

    print(f"Successfully recorded playing {title} on {start_time} for {playtime} minutes")

def play(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) < 3:
        print(f"Usage: play [title] [start date: {DATE_FORMAT}] [playtime in minutes]")
        return
    if 'uid' not in ctx:
        print("Not logged in. Login first!")
        return

    title = " ".join(args[0:-2])
    try:
        start_date = datetime.strptime(args[-2], DATE_FORMAT)
    except ValueError:
        print(f"failed: start date improperly formatted: it must be of the form {DATE_FORMAT}")
        return

    try:
        playtime = int(args[-1])
    except ValueError:
        print("failed: playtime not an int")
        return
    uid = ctx['uid']

    _play(conn, uid, title, start_date, playtime)


def play_random(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) == 0:
        print("Usage: play_random [collection]")
        return
    if 'uid' not in ctx:
        print("Not logged in. Login first!")
        return

    collection_name = " ".join(args)
    uid = ctx["uid"]

    with conn.cursor() as cur:
        cur.execute('''
            SELECT * FROM video_games
            WHERE vid=(
                SELECT vid FROM collection_has_video_game
                WHERE cid=(SELECT cid FROM collection WHERE name = %s)
                ORDER BY RANDOM()
                LIMIT 1
            )
        ''', (collection_name,))

        random_game = cur.fetchone()
        if not random_game:
            print("failed: collection is empty or doesn't exist")
            return

        print(f"Random game selected: {random_game[2]}")

        while True:
            try:
                duration = int(input("How many minutes did you play for? "))
                break
            except:
                print("Failed, try again.")
                continue
    start_time = datetime.now()
    _play(conn, uid, random_game[2], start_time, duration)
