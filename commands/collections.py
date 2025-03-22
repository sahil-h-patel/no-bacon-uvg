import psycopg
from typing import Any
# def example(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
#     print(f"args: {args}")
#     print(f"ctx: {ctx}")
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM users")
#         version = cur.fetchone()
#         print(f'Rows:{version}')
def collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
    if "uid" not in ctx:
        print("You are not logged in")
        return
    if args[0] == "create":
        create_collection(conn, args[1::], ctx)
    elif args[0] == "delete":
        delete_collection(conn, args[1::],  ctx)
    elif args[0] == "add":
        add_to_collection(conn, args[1::], ctx)
    elif args[0] == "remove":
        remove_from_collection(conn, args[1::], ctx)
    elif args[0] == "show":
        show_collections(conn, args[1::], ctx)
    elif args[0] == "count":
        count_collections(conn, args[1::], ctx)
    elif args[0] == "rename":
        rename_collection(conn, args[1::], ctx)    
    else: 
        return None
    
def create_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
    collectionName = input("Name: ")
    if len(collectionName) > 64:
        print("Colelction name should be less than 64 characters")
        return
    with conn.cursor() as cur:
        cur.execute(
        '''
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
        WHERE u.uid = %s AND c.name = %s;
        ''', 
        (ctx["uid"], collectionName))
        if cur.fetchone()[0] == "User does not have the collection":
            cur.execute(
            '''
            INSERT INTO collection (name)
            VALUES (%s)
            RETURNING cid;
            ''', 
            (collectionName,))
            cid = cur.fetchone()[0]
            cur.execute(
            '''
            INSERT INTO user_has_collection(uid, cid)
            VALUES(%s, %s)
            ''', 
            (ctx["uid"], cid))
        print(f'Successfully made collection {collectionName}')
        conn.commit()

def add_to_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
    col_name = input("Collection Name: ")
    if len(col_name) > 64:
        print("Colelction name should be less than 64 characters")
        return

    vg_name = input("Video Game Name: ")
    if len(vg_name) > 64:
        print("Video Game name should be less than 64 characters")
        return
    
    with conn.cursor() as cur:

        cur.execute('''
    SELECT vid
    FROM video_games
    WHERE title = %s;
    ''', (vg_name,))
        vg_id = cur.fetchone()[0]
        print("vg_id = ", vg_id)
        cur.execute('''
SELECT CASE 
           WHEN COUNT(*) > 0 THEN 'User has the platform for the video game'
           ELSE 'User does NOT have the platform for the video game'
       END AS result
FROM user_platform up
JOIN video_game_platforms vgp ON up.pid = vgp.pid
JOIN video_games vg ON vgp.vid = vg.vid
WHERE up.uid = %s -- Replace user_uid with the actual user's UID
  AND vg.title = %s; -- Replace 'VideoGameName' with the actual video game's name
        ''', (ctx["uid"], vg_name))
        res = cur.fetchone()[0]
        if res == "User does NOT have the platform for the video game":
            userAnswer = input("Warning you do not have the platform required for this game, would you like to continute (y/n)")
            if userAnswer != "y":
                return
        cur.execute('''
    SELECT cid
    FROM collection
    WHERE name = %s;
''', (col_name,))
        col_id = cur.fetchone()
        if not col_id:
            print("Collection does not exist")
            return
        col_id = col_id[0]
        print("col_id = ", col_id)
        cur.execute('''
INSERT INTO collection_has_video_game (cid, vid)
VALUES(%s, %s);
            ''', (col_id, vg_id))
        conn.commit()
        print("VideoGame successfully added")
        # version = cur.fetchone()
        # print(f'Rows:{version}')

def remove_from_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
    col_name = input("Collection Name: ")
    if len(col_name) > 64:
        print("Colelction name should be less than 64 characters")
        return

    vg_name = input("Video Game Name: ")
    if len(vg_name) > 64:
        print("Video Game name should be less than 64 characters")
        return

    with conn.cursor() as cur:
        cur.execute('''
    SELECT vid
    FROM video_games
    WHERE title = %s;
    ''', (vg_name,))
        vg_id = cur.fetchone()
        print("vg_id = ", vg_id)
        if not vg_id:
            print("Video Game does not exist")
            return
        vg_id = vg_id[0]

        cur.execute('''
    SELECT cid
    FROM collection
    WHERE name = %s;
''', (col_name,))
        col_id = cur.fetchone()  
        print("col_name = ", col_id)
        if not col_id:
            print("Collection does not exist")
            return
        col_id = col_id[0]
        cur.execute('''
    DELETE FROM collection_has_video_game WHERE cid = %s AND vid = %s
            ''', (col_id, vg_id))
        conn.commit()
        print("Successfully deleted")


def delete_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    col_name = input("Collection Name: ")
    if len(col_name) > 64:
        print("Colelction name should be less than 64 characters")
        return

    with conn.cursor() as cur:
        cur.execute('''
    SELECT cid
    FROM collection
    WHERE name = %s;
''', (col_name,))
        col_id = cur.fetchone() 
        print("col_name = ", col_id)
        if not col_id:
            print("Collection does not exist")
            return
        col_id = col_id[0]
    
        cur.execute(
        '''
        DELETE 
        FROM collection c
        WHERE cid = %s;
        ''',
        (col_id))
    print(f'Deleted collection successfully')
    conn.commit()

def rename_collection(conn: psycopg.Connection, args: list[str],  ctx: dict[str, Any]):
    old_name = input("Old collection Name: ")
    if len(old_name) > 64:
        print("Colelction name should be less than 64 characters")
        return
    new_name = input("New COllection Name:")
    if len(old_name) > 64:
        print("Collection name should be less than 64 characters")
        return
    
    with conn.cursor() as cur:
        cur.execute('''
    SELECT cid
    FROM collection
    WHERE name = %s;
''', (old_name,))
        col_id = cur.fetchone()
        # print("col_name = ", col_id)
        if not col_id:
            print("Collection does not exist")
            return
        col_id = col_id[0]

        cur.execute(
        '''
        UPDATE collection
        SET name = %s
        WHERE cid = %s;
        ''',
        (new_name, col_id))
    print(f'Renamed collection to {new_name} successfully')
    conn.commit() 

def count_collections(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
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
    user_id = ctx['uid']  # Assuming the user ID is passed as the first argument
    with conn.cursor() as curr:
        curr.execute(
        '''
        SELECT 
            c.name AS collection_name,
            COUNT(chvg.vid) AS number_of_video_games,
            COALESCE(SUM(EXTRACT(EPOCH FROM (up.end_time - up.start_time)) / 3600), 0) AS total_playtime_hours
        FROM collection c
        LEFT JOIN user_has_collection uhc ON c.cid = uhc.cid
        LEFT JOIN collection_has_video_game chvg ON c.cid = chvg.cid
        LEFT JOIN user_plays up ON chvg.vid = up.vid AND uhc.uid = up.uid
        WHERE uhc.uid = %s
        GROUP BY c.name
        ORDER BY c.name ASC;
        ''', 
        (user_id,))
        results = curr.fetchall()
    conn.commit()
    return results
    