import psycopg
from datetime import datetime
from typing import Any

DATE_FORMAT = "%m-%d-%Y"

def play(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) != 3:
        print(f"Usage: play [title] [start date: {DATE_FORMAT}] [end date: {DATE_FORMAT}]")
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
        end_date = datetime.strptime(args[-1], DATE_FORMAT)
    except ValueError:
        print(f"failed: start date improperly formatted: it must be of the form {DATE_FORMAT}")
        return
    uid = ctx['uid']

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
            ''', (uid, title, start_date, end_date))
        except psycopg.errors.NotNullViolation:
            print(f"failed: could not find video game named '{title}'")
            return
    conn.commit()

    print(f"Successfully recorded playing {title} from {start_date} to {end_date}")
