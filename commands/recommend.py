import psycopg
from typing import Any
from datetime import date, timedelta
import calendar

def top_20_rolling(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if (len(args) != 0):
        print("usage: top_5_monthly")
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
        for i in range(5):
            print(str(i+1) + ":\t" + result[i][2])

def top_20_followers(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    pass

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
                total DESC''', (date.today().replace(day=1) - timedelta(days=1),))
        
        print(calendar.month_name[date.today().month] + "'s Top 5 Games:")
        print("----------------------")
        result = cur.fetchall()
        for i in range(5):
            print(str(i+1) + ":\t" + result[i][2])

def for_you(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    pass