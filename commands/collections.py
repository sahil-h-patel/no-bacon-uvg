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
        cur.execute("""
SELECT 
    CASE 
        WHEN COUNT(c.cid) > 0 THEN 'User has the collection'
        ELSE 'User does not have the collection'
    END AS result
FROM 
    users u
JOIN 
    user_has_collection uhc
ON 
    u.uid = uhc.uid
JOIN 
    collection c
ON 
    uhc.cid = c.cid
WHERE 
    u.uid = %s AND c.name = '%s';

        """, (ctx["uid"], collectionName))
        if cur.fetchone == "User does not have the collection":
            cur.execute("""
    INSERT INTO collection (name)
        VALUES ('%s');
            """, collectionName)
            cur.execute("""
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
    print(f"args: {args}")
    print(f"ctx: {ctx}")
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        version = cur.fetchone()
        print(f'Rows:{version}')


def count_collections(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print(f"args: {args}")
    print(f"ctx: {ctx}")
    with conn.cursor() as cur:
        cur.execute("""
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
        """, ctx["uid"])
        version = cur.fetchone()
        print(f'Rows:{version}')
 