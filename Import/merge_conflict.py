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
    if not load_dotenv('../.env'):
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
    with db_conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO users (username,password,first_name,last_name,creation_date,last_access) VALUES (%s,%s,%s,%s,%s,CURRENT_TIMESTAMP) ON CONFLICT DO NOTHING", users)
        db_conn.commit()


def add_games():
    game_file = open('video_games.txt', 'r').readlines()
    games = []
    for line in game_file:
        games += [tuple(line.strip().split(','))]
    with db_conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO video_games (title,esrb) VALUES (%s,%s) ON CONFLICT DO NOTHING", games)
        db_conn.commit()


def add_genres():
    genre_file = open('genres.txt', 'r').readlines()
    genres = []
    for line in genre_file:
        genres += [tuple(line.strip('\n'))]
    with db_conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO genre (genre) VALUES (%s) ON CONFLICT DO NOTHING", genres)
        db_conn.commit()


def add_platform():
    platform_file = open('platforms.txt', 'r').readlines()
    platforms = []
    for line in platform_file:
        platforms += [tuple(line.strip('\n'))]
    with db_conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO platform (name) VALUES (%s) ON CONFLICT DO NOTHING", platforms)
        db_conn.commit()


def add_collection():
    collection_file = open('collection.txt', 'r').readlines()
    collections = []
    for line in collection_file:
        collections += [tuple(line.strip('\n'))]
    with db_conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO collection (name) VALUES (%s) ON CONFLICT DO NOTHING", collections)
        db_conn.commit()


def add_email():
    email_file = open('emails.txt', 'r').readlines()
    emails = []
    for line in email_file:
        emails += [tuple(line.strip('\n'))]
    with db_conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO user_email (uid,email) VALUES ((SELECT uid FROM users ORDER BY RANDOM() LIMIT 1),%s)  ON CONFLICT DO NOTHING", emails)
        db_conn.commit()


def add_contributors():
    contributor_file = open('contributors.txt', 'r').readlines()
    contributors = []
    for line in contributor_file:
        contributors += [tuple(line.strip('\n'))]
    with db_conn.cursor() as cur:
        cur.executemany(
            "INSERT INTO contributor (name) VALUES (%s) ON CONFLICT DO NOTHING", contributors)
        db_conn.commit()


def populate_user_has_collection():
    # Since have been randomly generated, must make sure no collection is ownerless
    with db_conn.cursor() as cur:
        cur.execute("""
            WITH uids AS (
                SELECT uid FROM users ORDER BY random()
            ),
                cids AS (
                SELECT cid FROM collection ORDER BY random()
            )
            INSERT INTO user_has_collection (uid, cid)
            SELECT u.uid, c.cid
            FROM uids u
            JOIN cids c ON random() < 0.5
            LIMIT 6000
            ON CONFLICT DO NOTHING
            """
                    )
        db_conn.commit()


def populate_video_game_platform():
    with db_conn.cursor() as cur:
        cur.execute("""
                SELECT vid FROM video_games ORDER BY random()
                ),
                    pids AS (
                    SELECT pid FROM platform ORDER BY random()
                )
                INSERT INTO video_game_platforms (vid, pid,price,release_date)
                SELECT vid, pid,
                floor(random() * 100) + 0.99 AS price,
                DATE '1990-01-01' + INTERVAL '1 day' * floor(random() * (DATE '2024-12-31' - DATE '1990-01-01')) AS release_date
                FROM vids v
                JOIN pids p ON random() < 0.5
                LIMIT 6000 
                ON CONFLICT DO NOTHING
        """)
        db_conn.commit()


def populate_collection_has_video_games():
    # collection must contain games that are in the user platform
    with db_conn.cursor() as cur:
        cur.execute("""
            WITH cids AS (
                SELECT cid FROM collection ORDER BY random()
            ),
                vids AS (
                SELECT vid FROM video_games ORDER BY random()
            )
            INSERT INTO collection_as_video_game (cid, vid)
            SELECT cid, vid
            FROM cids
            JOIN vids  ON random() < 0.5
            LIMIT 6000
            ON CONFLICT DO NOTHING
            """
                    )
        db_conn.commit()


def populate_user_platforms():
    # Random
    with db_conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_platform (uid, pid)
            SELECT u.uid, p.pid 
            FROM users u
            JOIN user_has_collection c ON c.uid = u.uid
            JOIN collection_has_video_game v ON v.cid = c.cid
            JOIN video_game_platforms p ON p.vid = v.vid
            ORDER BY RANDOM()
            ON CONFLICT DO NOTHING
            LIMIT 30000
            """
                    )
        db_conn.commit()


def populate_user_ratings():
    with db_conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_rating (uid, vid,rating)
            SELECT u.uid, v.vid, floor(random() * 5) + 1
            FROM users u
            JOIN user_has_collection c ON c.uid = u.uid
            JOIN collection_has_video_game v ON v.cid = c.cid
            ORDER BY RANDOM()
            LIMIT 5 
            ON CONFLICT DO NOTHING;            
            """
                    )
        db_conn.commit()

        """
            INSERT INTO user_rating (uid, vid,rating)
            SELECT u.uid, v.vid,
            NOW() - INTERVAL '1 day' * (random() * 365) AS start_time,
            (NOW() - INTERVAL '1 day' * (random() * 365)) + INTERVAL '1 minutes' * (random() * 10 + 1) AS end_time
            FROM users u
            JOIN user_has_collection c ON c.uid = u.uid
            JOIN collection_has_video_game v ON v.cid = c.cid
            ORDER BY RANDOM()
            LIMIT 10000 
            ON CONFLICT DO NOTHING;            

        """


def populate_user_ratings():
    with db_conn.cursor() as cur:
        cur.execute("""
            INSERT INTO user_rating (uid, vid,rating)
            SELECT u.uid, v.vid,
            NOW() - INTERVAL '1 day' * (random() * 365) AS start_time,
            (NOW() - INTERVAL '1 day' * (random() * 365)) + INTERVAL '1 minutes' * (random() * 10 + 1) AS end_time
            FROM users u
            JOIN user_has_collection c ON c.uid = u.uid
            JOIN collection_has_video_game v ON v.cid = c.cid
            ORDER BY RANDOM()
            LIMIT 6000 
            ON CONFLICT DO NOTHING;            
            """
                    )
        db_conn.commit()


def populate_video_game_genre():
    with db_conn.cursor() as cur:
        cur.execute("""
            WITH vids AS (
                SELECT vid FROM video_games ORDER BY random()
            ),
                gids AS (
                SELECT gid FROM genre ORDER BY random()
            )
            INSERT INTO video_game_genre (vid,gid)
            SELECT v.vid, g.gid
            FROM vids v
            JOIN gids g ON random() < 0.5 
            ORDER BY RANDOM()
            LIMIT 6000
            ON CONFLICT DO NOTHING
            """
                    )
        db_conn.commit()


def populate_video_game_developer():
    with db_conn.cursor() as cur:
        cur.execute("""
            WITH vid AS (
                SELECT vid FROM video_games ORDER BY random()
            ),
                dpids AS (
                SELECT dpid FROM contributor ORDER BY random()
            )
            INSERT INTO video_game_developer (vid,dpid)
            SELECT v.vid, d.dpid
            FROM vids v
            JOIN dpids d ON random() < 0.5 
            ORDER BY RANDOM()
            LIMIT 6000
            ON CONFLICT DO NOTHING
            """
                    )
        db_conn.commit()


def populate_video_game_publisher():
    with db_conn.cursor() as cur:
        cur.execute("""
            WITH vid AS (
                SELECT vid FROM video_games ORDER BY random()
            ),
                dpids AS (
                SELECT dpid FROM contributor ORDER BY random()
            )
            INSERT INTO video_game_publisher (vid,dpid)
            SELECT v.vid, d.dpid
            FROM vids v
            JOIN dpids d ON random() < 0.5 
            ORDER BY RANDOM()
            LIMIT 6000
            ON CONFLICT DO NOTHING
            """
                    )
        db_conn.commit()
