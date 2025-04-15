import psycopg
from typing import Any

from commands.collections import data_nonexistant

# def example(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
#     print(f"args: {args}")
#     print(f"ctx: {ctx}")
#     with conn.cursor() as cur:
#         cur.execute("SELECT * FROM users")
#         version = cur.fetchone()
#         print(f'Rows:{version}')

def platform(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if "uid" not in ctx:
        print("You are not logged in")
        return
    if len(args) < 1:
        print("Usage: platform [add|remove|show]")
        return
    if args[0] == "add":
        platform_add(conn, args[1::], ctx)
    elif args[0] == "remove":
        platform_remove(conn, args[1::], ctx)
    elif args[0] == "show":
        platform_show(conn, args[1::], ctx)


def platform_add(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) < 1:
        print("Usage: platform add [platform Name here]")
        return
    pl_name = " ".join(args)
    if len(pl_name) > 64:
        print("Platform name should not exceed 64 characters")
        return
    
    with conn.cursor() as cur:
        # ------------Query Boundary ----------------------
        # Check that platform exists
        datatype = "Platform"
        query = "SELECT COALESCE((select p.pid from platform p where p.name = %s LIMIT 1), -1);"
        pl_id = data_nonexistant(conn, ctx, query, datatype, pl_name)
        # print(pl_id," ",    ctx["uid"])
        if pl_id >= 0:
            cur.execute('''
                INSERT INTO user_platform (uid, pid)
                VALUES (%s, %s); ''', (ctx["uid"], pl_id))
            print(f"You now own {pl_name}!")
    conn.commit()
        


def platform_remove(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) < 1:
        print("Usage: platform remove [platform Name here]")
        return 
    pl_name = " ".join(args)
    if len(pl_name) > 64:
        print("Platform name should not exceed 64 characters")
        return
    
    with conn.cursor() as cur:
        # Check that platform exists
        datatype = "Platform"
        query = "SELECT COALESCE((select p.pid from platform p where p.name = %s), -1);"
        pl_id = data_nonexistant(conn, ctx, query, datatype, pl_name)
        # ------------Query Boundary ----------------------
        res = -1
        while res < 0:
            if res == -2:
                pl_name = input("Input a new Platform Name: ")
                datatype = "Platform"
                query = "SELECT COALESCE((select p.pid from platform p where p.name = %s), -1);"
                pl_id = data_nonexistant(conn, ctx, query, datatype, pl_name)
            # print(f"col_id = {col_id}")
            cur.execute('''
                SELECT COALESCE((SELECT uid from user_platform where uid = %s and pid = %s), -1);
            ''', (ctx["uid"], pl_id))
            res = cur.fetchone()[0]
            if res == -1:
                cur.execute('''SELECT count(*) from user_platform where uid = %s''', (ctx["uid"],))
                temp = cur.fetchone()[0]
                if temp == 0:
                    print("You don't own any Platforms")
                    return
                print("You don't own this Platform")
                res = -2
        # ------------Query Boundary ----------------------
        if pl_id >= 0:
            cur.execute('''
            DELETE FROM user_platform WHERE uid = %s AND pid = %s;
            ''', (ctx["uid"], pl_id))
            print("Platform successfully removed")
    conn.commit()
        
        
def platform_show(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) > 0:
        print("Usage: platform show")
        return 
    print("\nPlatforms:\n")
    with conn.cursor() as cur:
        query = '''
        select p.name from platform p 
        join user_platform up on p.pid = up.pid
        where up.uid = %s 
        '''
        cur.execute(query, (ctx["uid"],))
        results = cur.fetchall()
        if len(results) == 0:
            print("You don't own any Platforms, you can add them with command >platform add [platform name]")
            return
        for row in results:
            print(f"\t{row[0]}")

