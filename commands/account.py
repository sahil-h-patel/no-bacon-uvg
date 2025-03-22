import psycopg
from getpass import getpass
from typing import Any

def create_account(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) != 0:
        print("usage: create_account")
        return

    username = input("Username: ")
    email = input("Email: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    password = getpass()
    if password != getpass("Confirm password: "):
        print("Different passwords detected, aborting...")
        return

    with conn.cursor() as cur:
        try:
            cur.execute('''
                INSERT INTO users (username, password, first_name, last_name, creation_date, last_access)
                VALUES (%s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)
                RETURNING uid;
            ''', (username, password, first_name, last_name))
            user = cur.fetchone()
            if not user:
                print("Failed to create user")
                return

            cur.execute('''
                INSERT INTO user_email (uid, email)
                VALUES (%s, %s);
            ''', (user[0], email))
            conn.commit()
        except psycopg.errors.UniqueViolation:
            print("failed: Username already in use, aborting...")
            return
        except Exception as e:
            print(f"failed: {e}")
            return

    print(f"Successfully created new user '{username}'")

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
                username = %s
                AND password = %s;
        ''', (username, password))
        user = cur.fetchone()
        if not user:
            print("Invalid username or password.")
            return

        uid = user[0]

        cur.execute('''
            UPDATE
                users
            SET
                last_access = CURRENT_TIMESTAMP
            WHERE
                uid = %s;
        ''', (uid,))
        conn.commit()

        ctx["uid"] = uid
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
