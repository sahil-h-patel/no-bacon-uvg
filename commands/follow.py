import psycopg
from typing import Any

def follow(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(args)
    if (len(args) != 1):
        print("usage: follow [username]")
        return

    with conn.cursor() as cur:
        cur.execute('''
            SELECT 
                uid, username 
            FROM 
                users
            WHERE 
                username = '%s';
            '''% (args[0]))
        followee = cur.fetchone()
        if not followee:
            print("user not found")
            return
        
        cur.execute('''
            SELECT 
                followee_uid 
            FROM 
                follows
            WHERE 
                follower_uid = '%s'
                AND followee_uid = '%s';
            '''% (ctx['uid'], followee[0]))
        check = cur.fetchone()
        if check:
            print("you already follow this person (creep)")
            return

        cur.execute(f"INSERT INTO follows (follower_uid, followee_uid) VALUES ('{ctx['uid']}', '{followee[0]}')")
        print("User followed")
    conn.commit()