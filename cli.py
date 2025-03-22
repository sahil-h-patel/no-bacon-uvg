from sys import stdin, stdout
from dotenv import load_dotenv
from collections.abc import Callable
from typing import Any
import psycopg
import os
import sshtunnel as ssh
import atexit

from commands import (
    example, 
    follow, 
    login, 
    logout, 
    play, 
    unfollow, 
    create_account,
    collection,
)

PROMPT = "nbuvg> "
CMDS: dict[str, Callable[[psycopg.Connection, list[str], dict[str, Any]], None]] = {
    "example": example,
    "login": login,
    "logout": logout,
    "collection":collection,
    "play": play,
    "play_random": play_random,
    "rate": rate,
    "follow": follow,
    "unfollow": unfollow,
    "create_account": create_account,
}

CONTEXT: dict[str, Any] = {}

db_conn: psycopg.Connection | None = None
tunnel: ssh.SSHTunnelForwarder | None = None


def prompt():
    stdout.write(PROMPT)
    stdout.flush()


def setup_db_conn():
    ssh_host = os.getenv('SSH_HOST')
    ssh_user = os.getenv('SSH_USER')
    ssh_password = os.getenv('SSH_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT'))
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    global tunnel
    global db_conn

    tunnel = ssh.open_tunnel(
        (ssh_host, 22),  # SSH host and port
        ssh_username=ssh_user,
        ssh_password=ssh_password,  # Or use password authentication if needed
        # Remote database bind address and port
        remote_bind_address=(db_host, db_port)
    )
    tunnel.start()
    print("Successfully established a ssh tunnel")
    db_conn = psycopg.connect(
        f"host={db_host} port={tunnel.local_bind_port} dbname={
            db_name} user={db_user} password={db_password}"
    )
    print("Successfully connected to the database!")

    with db_conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        version = cur.fetchone()
        print(f'Rows:{version}')


def main():
    # Load .env
    if not load_dotenv('.env'):
        print("Failed to load .env\nCheck README.md for format")
        return

    # Setup connections
    setup_db_conn()

    if not db_conn or not tunnel:
        print("Failed to establish connection with DB")
        return

    prompt()
    for cmd in stdin:
        args = cmd.strip().split(" ")
        cmd = args[0]
        del args[0]

        if cmd == "exit":
            break
        if cmd in CMDS:
            db_conn.rollback()
            CMDS[cmd](db_conn, args, CONTEXT)
        else:
            print("Command not found :(")

        prompt()


def exit_handler():
    print("Shutting down the database connection...")
    if db_conn:
        db_conn.close()
    print("Shutting down the ssh tunnel...")
    if tunnel:
        tunnel.close()


if __name__ == '__main__':
    atexit.register(exit_handler)
    main()
