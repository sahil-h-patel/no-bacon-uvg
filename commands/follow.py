import psycopg
from typing import Any

def follow(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):

    '''
    Updates the database to include a relationship between the logged in user
    and the user represented by the username.

    Args:
        conn (psycopg.Connection): Database connection
        args (list[str]): Arguments passed to the method
        ctx (dict[str, Any]): Information about the current user

    Returns:
        None
    '''
    
    if len(args) != 1:
        print("usage: follow [email]")
        return
    if 'uid' not in ctx:
        print("must be logged in to use this command")
        return

    with conn.cursor() as cur:
        cur.execute('''
            SELECT 
                uid 
            FROM 
                user_email
            WHERE 
                email = %s;
            ''', (args[0],))
        followee = cur.fetchone()
        if not followee:
            print("email not found")
            return
        
        cur.execute('''
            SELECT 
                followee_uid 
            FROM 
                follows
            WHERE 
                follower_uid = %s
                AND followee_uid = %s;
            ''', (ctx['uid'], followee[0]))
        check = cur.fetchone()
        if check:
            print("you already follow this person (creep)")
            return

        cur.execute('''
            INSERT INTO 
                follows (follower_uid, followee_uid) 
            VALUES 
                (%s, %s)
            ''', (ctx['uid'], followee[0]))
    conn.commit()
    print("User followed")

def unfollow(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):

    '''
    Deletes from the database the relation between the logged in user and the 
    requested user.

    Args:
        conn (psycopg.Connection): Database connection
        args (list[str]): Arguments passed to the method
        ctx (dict[str, Any]): Information about the current user

    Returns:
        None
    '''

    if len(args) != 1:
        print("usage: unfollow [email]")
    if 'uid' not in ctx:
        print("must be logged in to use this command")
        return

    with conn.cursor() as cur:
        cur.execute('''
            SELECT 
                uid 
            FROM 
                user_email
            WHERE 
                email = %s;
            ''', (args[0],))
        followee = cur.fetchone()
        if not followee:
            print("email not found")
            return
        
        cur.execute('''
            SELECT 
                followee_uid 
            FROM 
                follows
            WHERE 
                follower_uid = %s
                AND followee_uid = %s;
        ''', (ctx['uid'], followee[0]))
        check = cur.fetchone()
        if not check:
            print("you do not follow this person")
            return
        
        cur.execute('''
            DELETE FROM 
                follows 
            WHERE 
                follower_uid = %s 
                AND followee_uid = %s;''', (ctx['uid'], followee[0]))
    conn.commit()
    print("User unfollowed")

def count_users_you_follow(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT COALESCE((SELECT count(follower_uid) from follows where follower_uid = %s), 0);
''', (ctx["uid"],))
        return cur.fetchone()[0]
    return 

def count_followers(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    with conn.cursor() as cur:
        cur.execute('''
        SELECT COALESCE((SELECT count(followee_uid) from follows where followee_uid = %s), 0);
''', (ctx["uid"],))
        return cur.fetchone()[0]
    return 