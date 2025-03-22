import psycopg
from typing import Any
from datetime import datetime
import sys

def search(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    title = input("Title: ")
    platform = input("Platform: ")
    print("dates in format (mm-dd-yyyy)")
    releaseDateStart = input("Release Date Start: ")
    try: datetime.strptime(releaseDateStart, "%m-%d-%Y")
    except: 
        print("invalid date, exiting")
        return
    releaseDateEnd = input("Release Date End: ")
    try: datetime.strptime(releaseDateEnd, "%m-%d-%Y")
    except: 
        print("invalid date, exiting")
        return
    developer = input("Developer: ")
    publisher = input("Publisher: ")
    price = input("Price: ")
    genre = input("Genre: ")

    # Type checking
    if price == "":
        price = sys.float_info.max
    if releaseDateEnd == "":
        releaseDateEnd = datetime.max
    if releaseDateStart == "":
        releaseDateStart = datetime.min
    
    # Get order style
    orderby = ""
    print("1: by price\n2: by genre\n3: by release year")
    choice = input("Change order: ")
    match choice:
        case "1":
            orderby = "ORDER BY\nvg_platform.price"
        #case "2":
        #    order = "ORDER BY genre ASC"
        case "3":
            orderby = "ORDER BY\nvg_platform.release_date"
        case _:
            orderby = "ORDER BY title ASC, vg_platform.release_date ASC"
    
    # Get ASC Vs. DESC
    print("1: ASC\n2: DESC")
    choice = input("ASC or DES: ")
    match choice:
        case "1":
            orderby = orderby + " ASC"
        case "2":
            orderby = orderby + "  DESC"

    with conn.cursor() as cur:
        cur.execute("""
            SELECT DISTINCT
                SUM(up.end_time - up.start_time) AS total_time,
                vg.vid AS vgid,
                vg.Title AS video_game_name
            FROM
                video_games vg
            JOIN
                video_game_platforms vg_platform ON vg.vid = vg_platform.vid
            JOIN
                platform p ON vg_platform.pid = p.pid
            LEFT JOIN
                video_game_developer vg_dev ON vg.vid = vg_dev.vid
            LEFT JOIN
                contributor dev ON vg_dev.dpid = dev.dpid
            LEFT JOIN
                video_game_publisher vg_pub ON vg.vid = vg_pub.vid
            LEFT JOIN
                contributor pub ON vg_pub.dpid = pub.dpid
            LEFT JOIN
                user_plays up ON vg.vid = up.vid
            LEFT JOIN
                user_rating ur ON vg.vid = ur.vid
            LEFT JOIN
                video_game_genre vg_genre ON vg.vid = vg_genre.vid
            LEFT JOIN
                genre g ON vg_genre.gid = g.gid
            WHERE
                vg.Title ILIKE %s ESCAPE ''
                AND p.name ILIKE %s ESCAPE ''
                AND dev.name ILIKE %s ESCAPE ''
                AND pub.name ILIKE %s ESCAPE ''
                AND g.genre ILIKE %s ESCAPE ''
                AND vg_platform.price <= %s
                AND vg_platform.release_date >= %t
                AND vg_platform.release_date <= %t
            GROUP BY
                vgid, video_game_name
            """,("%"+title+"%","%"+platform+"%","%"+developer+"%","%"+publisher+"%","%"+genre+"%",int(price),releaseDateStart,releaseDateEnd))
        
        work = cur.fetchall()
        for i in work:
            print("Name: " + str(i[2]))
            print("Time Played: " + str(i[0]))
            cur.execute("SELECT * FROM platform WHERE pid IN (SELECT pid FROM video_game_platforms WHERE vid=%s)",(i[1],))
            print("Platforms: " + str(cur.fetchall()[0]))
            cur.execute("SELECT * FROM contributor WHERE dpid IN (SELECT dpid FROM video_game_developer WHERE vid=%s)",(i[1],))
            print("Developers: " + str(cur.fetchall()[0]))
            cur.execute("SELECT * FROM contributor WHERE dpid IN (SELECT dpid FROM video_game_publisher WHERE vid=%s)",(i[1],))
            print("Producers: " + str(cur.fetchall()[0]))
            cur.execute("SELECT u.username, ur.rating FROM user_rating AS ur, users AS u WHERE ur.vid=%s AND u.uid=ur.uid",(i[1],))
            print("Ratings: " + str(cur.fetchall()[0]))
            cur.execute("SELECT * FROM genre AS g WHERE g.gid IN (SELECT gid FROM video_game_genre WHERE vid=%s)",(i[1],))
            print("Genres: " + str(cur.fetchall()[0]))
            print()
        