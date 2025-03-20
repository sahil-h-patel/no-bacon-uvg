import psycopg
from getpass import getpass
from typing import Any

def login(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) != 1:
        print("usage: login [username]")
        return
    if "uid" in ctx:
        print("Already logged in. Try logging out before logging in to a different user.")
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

def logout(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) != 0:
        print("usage: logout")
        return
    if "uid" not in ctx:
        print("Not logged in.")
        return

    del ctx["uid"]
    print("Successfully logged out")
