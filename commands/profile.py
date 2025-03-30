import psycopg
from typing import Any

from commands.collections import count_collections

def profile(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if not ctx["uid"]:
        print("You're not logged in")
        return
    with conn.cursor() as cur:
        cur.execute('''SELECT username from users where uid = %s''', (ctx["uid"],))
        username = cur.fetchone()[0]
        print(f"Welcome to your Profile {username}!!")
        count_collections(conn, args, ctx)
        # Top 10 Followers ?
        print("Your top 10 Followers by Most Recent Access")
        cur.execute('''
            SELECT u.username, f.follower_uid, followee_uid from users u
                JOIN follows f on f.followee_uid = u.uid
                JOIN users u2 on f.follower_uid = u2.uid
            WHERE f.followee_uid = %s ORDER BY u.last_access LIMIT 10;    
        ''', (ctx["uid"],))

        result = cur.fetchall()
        # print(result)
        for res in result:
            print(f"\tUser: {res[0]}; Last Accessed: {res[1]}")
        if not result:
            print("Such empty, go make friends")
        print("\n\n")
        return