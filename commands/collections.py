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
    if len(args) == 0:
        print("collection [create|delete|add|remove|show|count|rename]")
        return
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
    elif args[0] == "describe":
        describe_collection(conn, args[1::], ctx)
    # elif args[0] == 'test':
    #     test(conn, args[1::], ctx)
    else: 
        return None
    
def create_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
    if len(args) < 1:
        print(f"Usage: collection create [Name]")
        return
    collectionName = " ".join(args)
    if len(collectionName) > 64:
        print("Collection name should be less than 64 characters")
        return
    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        cur.execute(
        '''
        SELECT 
            CASE 
                WHEN COUNT(c.cid) > 0 THEN 'Collection exists'
                ELSE 'Collection does not exist'
            END AS result
        FROM collection c 
        WHERE c.name = %s
        ''', 
        (collectionName,))
        res = cur.fetchone()[0]
        while res == "Collection exists":
            temp = input(f"Collection with name {collectionName} already exists, please choose a new name: ")
            cur.execute(
        '''
        SELECT 
            CASE 
                WHEN COUNT(c.cid) > 0 THEN 'Collection exists'
                ELSE 'Collection does not exist'
            END AS result
        FROM collection c 
        WHERE c.name = %s
        ''', 
        (temp,))
            res = cur.fetchone()[0]
            collectionName = temp
# ------------Query Boundary ----------------------
        if res == "Collection does not exist":
            cur.execute(
            '''
            INSERT INTO collection (name)
            VALUES (%s)
            RETURNING cid;
            ''', 
            (collectionName,))
            
# ------------Query Boundary ----------------------
            cid = cur.fetchone()[0]
            cur.execute(
            '''
            INSERT INTO user_has_collection(uid, cid)
            VALUES(%s, %s)
            ''', 
            (ctx["uid"], cid))
# ------------Query Boundary ----------------------
            print(f'Successfully made collection {collectionName}')
            conn.commit()
        else: 
            print(f'Collection creation failed: Collection with name "{collectionName}" Already exists')

def add_to_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
    if len(args) < 1:
        print(f"Usage: collection add [Video Game Name]")
        return
    vg_name = " ".join(args)
    if len(vg_name) > 64:
        print("Video Game name should be less than 64 characters")
        return

    col_name = input("Collection Name: ")
    if len(col_name) > 64:
        print("Collection name should be less than 64 characters")
        return
    
    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        res = -2
        while res < 0:
            temp = ""
            if res == -2:
                temp = input(f"Video game with name {vg_name} does not exist, double check that you spelled it correctly\n please choose a new name: ")
            cur.execute(
        '''
        SELECT COALESCE((select v.vid from video_games v where v.title = %s), -1);
        ''', 
        (temp,))
            res = cur.fetchone()[0]
            vg_name = temp
        vg_id = res

        # print("vg_id = ", vg_id)
# ------------Query Boundary ----------------------
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
# ------------Query Boundary ----------------------
        cur.execute('''
            SELECT cid
            FROM collection
            WHERE name = %s;
        ''', (col_name,))
# ------------Query Boundary ----------------------
        col_id = cur.fetchone()
        # print("col_id = ", col_id)
        if not col_id:
            print("Collection does not exist")
            return
        col_id = col_id[0]
        # print("col_id = ", col_id)
        res = -1
        while res < 0:
            if res == -2:
                
                col_name = input("Input new Collection Name:")
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

            cur.execute('''
                SELECT COALESCE((SELECT uid from user_has_collection where uid = %s and cid = %s), -1);
            ''', (ctx["uid"], col_id))
            temp = cur.fetchone()[0]
            if temp == -1:
                print("You don't own this collection")
                res = -2

# ------------Query Boundary ----------------------
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
        print("Collection name should be less than 64 characters")
        return

    vg_name = input("Video Game Name: ")
    if len(vg_name) > 64:
        print("Video Game name should be less than 64 characters")
        return

    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        cur.execute('''
    SELECT vid
    FROM video_games
    WHERE title = %s;
    ''', (vg_name,))
# ------------Query Boundary ----------------------
        vg_id = cur.fetchone()
        print("vg_id = ", vg_id)
        if not vg_id:
            print("Video Game does not exist")
            return
        vg_id = vg_id[0]

# ------------Query Boundary ----------------------
        cur.execute('''
    SELECT cid
    FROM collection
    WHERE name = %s;
''', (col_name,))
# ------------Query Boundary ----------------------
        col_id = cur.fetchone()  
        print("col_name = ", col_id)
        if not col_id:
            print("Collection does not exist")
            return
        col_id = col_id[0]
# ------------Query Boundary ----------------------
        cur.execute('''
    DELETE FROM collection_has_video_game WHERE cid = %s AND vid = %s
            ''', (col_id, vg_id))
        conn.commit()
        print("Successfully deleted")


def delete_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    col_name = input("Collection Name: ")
    if len(col_name) > 64:
        print("Collection name should be less than 64 characters")
        return

    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        cur.execute('''
    SELECT cid
    FROM collection
    WHERE name = %s;
''', (col_name,))
# ------------Query Boundary ----------------------
        col_id = cur.fetchone() 
        print("col_name = ", col_id)
        if not col_id:
            print("Collection does not exist")
            return
        col_id = col_id[0]
    
# ------------Query Boundary ----------------------
        cur.execute(
        '''
        DELETE 
        FROM collection c
        WHERE cid = %s;
        ''',
        (col_id,))
# ------------Query Boundary ----------------------
    print('Deleted collection successfully')
    conn.commit()

def rename_collection(conn: psycopg.Connection, args: list[str],  ctx: dict[str, Any]):
    old_name = input("Old collection Name: ")
    if len(old_name) > 64:
        print("Collection name should be less than 64 characters")
        return
    new_name = input("New COllection Name:")
    if len(old_name) > 64:
        print("Collection name should be less than 64 characters")
        return
    
    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        cur.execute('''
    SELECT cid
    FROM collection
    WHERE name = %s;
''', (old_name,))
# ------------Query Boundary ----------------------
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
# ------------Query Boundary ----------------------
    print(f'Renamed collection to {new_name} successfully')
    conn.commit() 

def count_collections(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    # print(f"args: {args}")
    # print(f"ctx: {ctx}")
    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        cur.execute(
        '''
        SELECT 
            COUNT(uhc.cid)  as total_collections
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
        (ctx["uid"],))
# ------------Query Boundary ----------------------
        count = cur.fetchone()
        if not count:
            print("failed to get count")
            return
        print(f'You have {count[0]} collections')

def show_collections(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    user_id = ctx['uid']  # Assuming the user ID is passed as the first argument
    with conn.cursor() as curr:
# ------------Query Boundary ----------------------
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
# ------------Query Boundary ----------------------
        results = curr.fetchall()
        for row in results:
            print(f"{row[0]} - {row[1]} video games - {row[2]} hours")
    return results


def describe_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    
    return ""

# def test(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
#     query = "SELECT COALESCE((SELECT uid from user_has_collection where uid = %s and cid = %s), -1);"
#     data = data_nonexistant(conn, ctx, query, "Collection", ctx["uid"], 1218)
#     print(f"{data} should be equal to 2010")

#     return ""


def data_nonexistant(conn: psycopg.Connection, ctx: dict[str, Any], query, datatype, *args):
    with conn.cursor() as cur:
        res = -2
        while res < 0:
            if res == -1:
                temp = input(f"\n{datatype} does not exist. Please double check your spelling and capitals\n Enter name here: ")
            cur.execute(query, (args))
            res = cur.fetchone()[0]
        return res
                
