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
        print("collection [create|delete|add|remove|show|count|rename|describe]")
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
        query = "SELECT COALESCE((select v.vid from video_games v where v.title = %s), -1);" 
        datatype = "Video Game"
        vg_id = data_nonexistant(conn, ctx, query, datatype, vg_name)
# ------------Query Boundary ----------------------
        # Making sure the User has the Platform for the game
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
        query = "SELECT cid FROM collection WHERE name = %s"
        datatype = "Collection"
        col_id = data_nonexistant(conn, ctx, query, datatype, col_name)

#   Making sure the User owns the Collection
        res = -1
        while res < 0:
            if res == -2:
                col_name = input("Input a new Collection Name: ")
                query = "SELECT cid FROM collection WHERE name = %s"
                datatype = "Collection"     
                col_id = data_nonexistant(conn, ctx, query, datatype, col_name)
            # print(f"col_id = {col_id}")
            cur.execute('''
                SELECT COALESCE((SELECT uid from user_has_collection where uid = %s and cid = %s), -1);
            ''', (ctx["uid"], col_id))
            res = cur.fetchone()[0]
            if res == -1:
                print("You don't own this collection")
                res = -2
# ------------Query Boundary ----------------------
        # I may have forgotten to check if the video game is already in the collection
        cur.execute('''
            SELECT COALESCE((SELECT vid from collection_has_video_game where cid = %s and vid = %s), -1);
        ''', (col_id, vg_id))
        res = cur.fetchone()[0]
        if res != -1:
            print(f"Collection {col_name} already has game {vg_name} in it :/")
            return
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
    if len(args) < 1:
        print(f"Usage: collection remove [Video Game Name]")
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
        query = "SELECT COALESCE((select v.vid from video_games v where v.title = %s), -1);" 
        datatype = "Video Game"
        vg_id = data_nonexistant(conn, ctx, query, datatype, vg_name)
# ------------Query Boundary ----------------------
        query = "SELECT cid FROM collection WHERE name = %s"
        datatype = "Collection"
        col_id = data_nonexistant(conn, ctx, query, datatype, col_name)

#   Making sure the User owns the Collection
        res = -1
        while res < 0:
            if res == -2:
                col_name = input("Input a new Collection Name: ")
                query = "SELECT cid FROM collection WHERE name = %s"
                datatype = "Collection"     
                col_id = data_nonexistant(conn, ctx, query, datatype, col_name)
            # print(f"col_id = {col_id}")
            cur.execute('''
                SELECT COALESCE((SELECT uid from user_has_collection where uid = %s and cid = %s), -1);
            ''', (ctx["uid"], col_id))
            res = cur.fetchone()[0]
            if res == -1:
                print("You don't own this collection")
                res = -2
# ------------Query Boundary ----------------------
        cur.execute('''
    DELETE FROM collection_has_video_game WHERE cid = %s AND vid = %s
            ''', (col_id, vg_id))
        conn.commit()
        print("Successfully deleted")


def delete_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) < 1:
        print(f"Usage: collection delete [Collection Name]")
        return
    col_name = " ".join(args)
    if len(col_name) > 64:
        print("Collection name should be less than 64 characters")
        return 

    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        query = "SELECT cid FROM collection WHERE name = %s"
        datatype = "Collection"
        col_id = data_nonexistant(conn, ctx, query, datatype, col_name)

#   Making sure the User owns the Collection
        res = -1
        while res < 0:
            if res == -2:
                col_name = input("Input a new Collection Name: ")
                query = "SELECT cid FROM collection WHERE name = %s"
                datatype = "Collection"     
                col_id = data_nonexistant(conn, ctx, query, datatype, col_name)
            # print(f"col_id = {col_id}")
            cur.execute('''
                SELECT COALESCE((SELECT uid from user_has_collection where uid = %s and cid = %s), -1);
            ''', (ctx["uid"], col_id))
            res = cur.fetchone()[0]
            if res == -1:
                print("You don't own this collection")
                res = -2    
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
    if len(args) < 1:
        print(f"Usage: collection rename [Collection Name]")
        return
    col_name = " ".join(args)
    if len(col_name) > 64:
        print("Collection name should be less than 64 characters")
        return 
    new_name = input("New Collection Name: ")
    if len(new_name) > 64:
        print("Collection name should be less than 64 characters")
        return
    
    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        query = "SELECT cid FROM collection WHERE name = %s"
        datatype = "Collection"
        col_id = data_nonexistant(conn, ctx, query, datatype, col_name)

#   Making sure the User owns the Collection
        res = -1
        while res < 0:
            if res == -2:
                col_name = input("Input a new Collection Name: ")
                query = "SELECT cid FROM collection WHERE name = %s"
                datatype = "Collection"     
                col_id = data_nonexistant(conn, ctx, query, datatype, col_name)
            # print(f"col_id = {col_id}")
            cur.execute('''
                SELECT COALESCE((SELECT uid from user_has_collection where uid = %s and cid = %s), -1);
            ''', (ctx["uid"], col_id))
            res = cur.fetchone()[0]
            if res == -1:
                print("You don't own this collection")
                res = -2    
        
# ------------Query Boundary ----------------------
        cur.execute('''SELECT COALESCE((SELECT cid from collection where name = %s),-1)''', (new_name,))
        res = cur.fetchone()[0]
        if res != -1:
            print("unfortunately that name is taken")
            return
# ------------Query Boundary ----------------------
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
    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        cur.execute(
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
        results = cur.fetchall()
        for row in results:
            print(f"{row[0]} - {row[1]} video games - {row[2]:.2f} hours")
    return results


def describe_collection(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) < 1:
        print(f"Usage: collection describe [Collection Name]")
        return
    col_name = " ".join(args)
    if len(col_name) > 64:
        print("Collection name should be less than 64 characters")
        return 
    with conn.cursor() as cur:
# ------------Query Boundary ----------------------
        query = "SELECT cid FROM collection WHERE name = %s"
        datatype = "Collection"
        col_id = data_nonexistant(conn, ctx, query, datatype, col_name)
        print(f"{col_name}")
# ------------Query Boundary ----------------------
        # Finding all the video games
        query = '''
select vg.title AS video_game_title,
    COALESCE(EXTRACT(EPOCH FROM (up.end_time - up.start_time))/3600, 0) AS playtime_in_hours
    from user_has_collection uhc
        JOIN collection c on uhc.cid = c.cid
        JOIN collection_has_video_game chvg ON c.cid = chvg.cid
        JOIN video_games vg on chvg.vid = vg.vid
        JOIN user_plays up ON vg.vid = up.vid
    WHERE up.uid = %s AND c.name = %s;
        '''
        cur.execute(query, (ctx["uid"], col_name))
        results = cur.fetchall()
        if len(results) == 0:
            print("No playtime in your games yet L bozo")
        for row in results:
            print(f"{row[0]} - {row[1]:.2f} hours")

# def test(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
#     query = "SELECT COALESCE((SELECT uid from user_has_collection where uid = %s and cid = %s), -1);"
#     data = data_nonexistant(conn, ctx, query, "Collection", ctx["uid"], 1218)
#     print(f"{data} should be equal to 2010")

#     return ""


def data_nonexistant(conn: psycopg.Connection, ctx: dict[str, Any], query, datatype, *args):
    with conn.cursor() as cur:
        # print(f"query, datatype, *args = {query}, {datatype}, *{args}")
        res = -2
        while res < 0:
            if res == -1:
                temp = input(f"\n{datatype} does not exist. Please double check your spelling and capitals\n Enter name here: ")
                args = list(args)
                args[0] = temp
                args = tuple(args)
            cur.execute(query, args)
            res = cur.fetchone()
            if not res:
                res = -1
                continue
            res = res[0]
        return res
                
