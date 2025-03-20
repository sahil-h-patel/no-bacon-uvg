import psycopg
from getpass import getpass
from typing import Any

def login(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) != 1:
        print("usage: login [username]")
        return

    username = args[0]
    password = getpass()

    with conn.cursor() as cur:
        cur.execute('''
            SELECT
                uid, username, password
            FROM
                users
            WHERE
                username = %s -- Replace with the entered username
                AND password = %s; -- Replace with the entered password
        ''', (username, password))
        user = cur.fetchone()
        if not user:
            print("Invalid username or password.")
            return
        ctx["uid"] = user[0]
        print(f"Successfully logged in as '{user[1]}'")
