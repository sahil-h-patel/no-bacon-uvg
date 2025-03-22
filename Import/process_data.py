from random import randint, random, choices, choice
from datetime import date, timedelta
from sys import stdin, stdout
from dotenv import load_dotenv
import psycopg
import os
import sshtunnel as ssh
import textwrap
import string
from datetime import date, datetime


def setup_conn():
    if not load_dotenv('.env'):
        print("Failed to load .env\nCheck README.md for format")
        exit()

    global db_conn
    ssh_host = os.getenv('SSH_HOST')
    ssh_user = os.getenv('SSH_USER')
    ssh_password = os.getenv('SSH_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    db_port = int(os.getenv('DB_PORT'))
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

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


def add_users():
    user_file = open('users.txt', 'r').readlines()
    users = []
    for line in user_file:
        users += [tuple(line.strip().split(',') +
                        [date(randint(2000, 2025), randint(1, 12), randint(1, 28))])]
    return
    with db_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (username,password,first_name,last_name,creation_date,last_access) VALUES (%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)", users)
        db_conn.commit()


def add_games():
    game_file = open('video_games.txt', 'r').readlines()
    games = []
    for line in game_file:
        games += [tuple(line.strip().split(','))]
    exit()
    with db_conn.cursor() as cur:
        cur.execute(
            "INSERT INTO video_games (title,esrb) VALUES (%s,%x)", games)
        db_conn.commit()


def populate_user_platforms():
    # Random
    with db_conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_platforms (uid, pid)
            SELECT
                (SELECT uid FROM users ORDER BY RANDOM() LIMIT 1),
                (SELECT pid FROM platforms ORDER BY RANDOM() LIMIT 1),
            FROM generate_series(1, 5000) 
            ON CONFLICT DO NOTHING; 
            """
                    )


def populate_user_has_collection():
    # Since have been randomly generated, must make sure no collection is ownerless
    with db_conn.cursor() as cur:
        cur.execute("""
            shuffles_cids AS (
                SELECT cid
                FROM collection
                ORDER BY RANDOM()
                LIMIT 5000 
            )
            INSERT INTO user_has_collection (uid, cid)
            SELECT
                (SELECT uid FROM users ORDER BY RANDOM() LIMIT 1),
                cid,
            FROM shuffled_cids;
            """)
        # db_conn.commit()


# def populate_user_rating():
#     # User must have the game to rate, so user_has_collection and user_has_game
#     with db_conn.cursor() as cur:
#         cur.execute("""
#             INSERT INTO user_rating (uid, vid, rating)
#             SELECT
#                 (SELECT uid FROM users ORDER BY RANDOM() LIMIT 1),
#                 (SELECT vid FROM video_games ORDER BY RANDOM() LIMIT 1),
#                 (SELECT unnest(enum_range(NULL::rating_scale)) ORDER BY random() LIMIT 1)
#             FROM generate_series(1, 5000)
#             ON CONFLICT DO NOTHING;
#             """
#                     )
#         # db_conn.commit()
#

def populate_collection_has_video_games():
    # Random
    with db_conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_rating (cid, vid)
            SELECT
                (SELECT cid FROM collection ORDER BY RANDOM() LIMIT 1),
                (SELECT vid FROM video_games ORDER BY RANDOM() LIMIT 1),
            FROM generate_series(1, 5000) 
            ON CONFLICT DO NOTHING; 
            """
                    )


# def populate_user_plays():
#     with db_conn.cursor() as cur:
#         cur.execute("""
#             INSERT INTO user_plays (uid,vid)
#         """)
#         db_conn.commit()


# setup_conn()
# add_users()
# add_games()
