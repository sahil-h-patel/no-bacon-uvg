import psycopg
from typing import Any
# def example(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
#     print(f"args: {args}")
#     print(f"ctx: {ctx}")
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM users")
#         version = cur.fetchone()
#         print(f'Rows:{version}')

def create_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(f"args: {args}")
    print(f"ctx: {ctx}")
    collectionName = args[0]
    with conn.cursor() as cur:
        cur.execute(
        """
        SELECT 
            CASE 
                WHEN COUNT(c.cid) > 0 THEN 'User has the collection'
                ELSE 'User does not have the collection'
            END AS result
        FROM users u
        JOIN user_has_collection uhc
        ON u.uid = uhc.uid
        JOIN collection c
        ON uhc.cid = c.cid
        WHERE u.uid = %s AND c.name = '%s';
        """, 
        (ctx["uid"], collectionName))
        if cur.fetchone == "User does not have the collection":
            cur.execute(
            """
            INSERT INTO collection (name)
                VALUES ('%s');
                    """, collectionName)
            cur.execute(
            """
            INSERT INTO user_has_collection(uid, cid)
            VALUES(%s, %s)
            """, )
        version = cur.fetchone()
        print(f'Rows:{version}')

def add_to_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(f"args: {args}")
    print(f"ctx: {ctx}")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        version = cur.fetchone()
        print(f'Rows:{version}')

def remove_from_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(f"args: {args}")
    print(f"ctx: {ctx}")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        version = cur.fetchone()
        print(f'Rows:{version}')

def delete_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    cid = args[0]
    with conn.cursor() as curr:
        curr.execute(
        '''
        DELETE 
        FROM collection c
        WHERE cid = %s;
        '''
        (cid))
    print(f'Deleted collection successfully')
    conn.commit()
    pass

def rename_collection(conn: psycopg.Connection, args: list[str]):
    name = args[0]
    cid = args[1]
    with conn.cursor() as curr:
        curr.execute(
        '''
        UPDATE collection
        SET name = %s
        WHERE cid = %s;
        '''
        (name, cid))
    print(f'Renamed collection to {name} successfully')
    conn.commit() 

def count_collections(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(f"args: {args}")
    print(f"ctx: {ctx}")
    with conn.cursor() as cur:
        cur.execute(
        '''
        SELECT 
            u.username  as user_name,
            count(uhc.cid)  as total_collections
        FROM 
            users u
        LEFT JOIN 
            user_has_collection uhc ON u.uid = uhc.uid
        WHERE u.uid = %s
        GROUP BY 
            u.username
        ORDER BY 
            total_collections DESC ;        
        ''', 
        ctx["uid"])
        version = cur.fetchone()
        print(f'Rows:{version}')

def show_collections(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    user_id = ctx['user_id']  # Assuming the user ID is passed as the first argument
    with conn.cursor() as curr:
        curr.execute(
        '''
        SELECT 
            c.name AS collection_name,
            COUNT(chvg.vid) AS number_of_video_games,
            COALESCE(SUM(EXTRACT(EPOCH FROM (up.end_time - up.start)) / 3600), 0) AS total_playtime_hours
        FROM collection c
        LEFT JOIN user_has_collection uhc ON c.cid = uhc.cid
        LEFT JOIN collection_has_video_game chvg ON c.cid = chvg.cid
        LEFT JOIN user_plays up ON chvg.vid = up.vid AND uhc.uid = up.uid
        WHERE uhc.uid = %s
        GROUP BY c.name
        ORDER BY c.name ASC;
        ''', 
        (user_id))
        results = curr.fetchall()
    conn.commit()
    return results
    