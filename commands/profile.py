import psycopg
from typing import Any

def profile(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if not ctx["uid"]:
        print("You're not logged in")
        return
    with conn.cursor() as cur:
        cur.execute('''SELECT username from users where uid = %s''', (ctx["uid"],))
        username = cur.fetchone()[0]
        print(f"Welcome to your Profile {username}!!")
        

        return