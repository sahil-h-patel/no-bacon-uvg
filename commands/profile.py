import psycopg
from typing import Any

from commands.collections import count_collections
from commands.follow import count_followers, count_users_you_follow

def profile(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if not ctx["uid"]:
        print("You're not logged in")
        return
    with conn.cursor() as cur:
        cur.execute('''SELECT username from users where uid = %s''', (ctx["uid"],))
        username = cur.fetchone()[0]
        print(f"Welcome to your Profile {username}!!")
        count_collections(conn, args, ctx)
        # Top 10 Video Games
        followers = count_followers(conn, args, ctx)
        you_follow = count_users_you_follow(conn, args, ctx)
        print(f"You Follow {you_follow} many Users, and {followers} follow you\n")
        print("Your top 10 Video Games by Playtime")
            # SELECT v.title from video_games
            #         LEFT JOIN user_has_video_game uhvg on v.vid = uhvg.vid
            #     where uhvg.uid = %s 
        # Realizing that a User doesn't have a video game and thats just not in the schema so every user needs to have a collection that holds their video games
        cur.execute('''
                    
            SELECT u.username, f.follower_uid, followee_uid from users u
                JOIN follows f on f.followee_uid = u.uid
                JOIN users u2 on f.follower_uid = u2.uid
            WHERE f.followee_uid = %s ORDER BY u.last_access LIMIT 10;    
        ''', (ctx["uid"],))

        result = cur.fetchall()
        # print(result)
        for res in result:
            print(f"\tVideo Game: {res[0]}; Playtime: {res[1]}")
        if not result:
            print("Such empty, go make friends")
        print("\n")
        return