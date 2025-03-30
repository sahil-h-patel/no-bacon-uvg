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

        cur.execute('''
SELECT 
    vg.title AS video_game_title,
    SUM(EXTRACT(EPOCH FROM (up.end_time - up.start_time))/3600) AS total_playtime_in_hours
FROM 
    user_plays up
JOIN 
    video_games vg ON up.vid = vg.vid
WHERE 
    up.uid = %s
GROUP BY 
    vg.title
ORDER BY 
    total_playtime_in_hours DESC
LIMIT 10;

        ''', (ctx["uid"],))

        result = cur.fetchall()
        # print(result)
        for res in result:
            print(f"\tVideo Game: {res[0]}; Playtime: {res[1]}")
        if not result:
            print("Such empty, go play games")
        print("\n")
        return