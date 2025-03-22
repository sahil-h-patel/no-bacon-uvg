import psycopg
from typing import Any
from datetime import datetime
'''
Users will be able to search for video games by 
    name
    platform
    release date
    developers
    price
    genre
The resulting list of video games must show 
    the video game’s name
    platforms
    the developers
    the publisher
    the playtime
    the ratings (age and user)
The list must be sorted alphabetically (ascending) by video game’s name and release date. 
Users can sort the resulting list by: 
    video game name
    price
    genre
    released year (ascending and descending)
'''


def search(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    title = input("Title: ")
    platform = input("Platform: ")
    print("dates in format (mm dd yyyy)")
    releaseDateStart = input("Release Date Start: ")
    releaseDateEnd = input("Release Date End: ")
    developer = input("Developer: ")
    publisher = input("Publisher: ")
    price = input("Price: ")
    genre = input("Genre: ")

    # Type checking
    if price == "":
        price = "0"
    
    '''
    print("1: by price\n2: by genre\n3: by release year")
    choice = input("Change order: ")
    match choice:
        case "":
            order = "ORDER BY title"
        case "1":
            order = "ORDER BY price"
        case "2":
            order = "ORDER BY genre"
        case "3":
            order = "ORDER BY released year"
    print("1: ASC\n2: DESC")
    choice = input("ASC or DES: ")
    match choice:
        case "1":
            order = order + "ASC"
        case "2":
            order = order + "DESC"
    '''
    
    order = """ORDER BY title ASC"""
    with conn.cursor() as cur:
        cur.execute("""
            SELECT
                vg.Title AS video_game_name,
                p.name AS platform_name,
                d.name AS developer_name,
                pub.name AS publisher_name,
                vg_platform.price AS Price,
                vg_platform.release_date AS release_date,
                vg.ESRB AS age_rating,
                ur.rating AS user_rating,
                AVG(EXTRACT(EPOCH FROM (up.end_time - up.start)) / 3600) AS average_playtime_hours
            FROM
                video_games vg
            JOIN
                video_game_platforms vg_platform ON vg.vid = vg_platform.vid
            JOIN
                platform p ON vg_platform.pid = p.pid
            LEFT JOIN
                video_game_developer vg_dev ON vg.vid = vg_dev.vid
            LEFT JOIN
                contributor d ON vg_dev.dpid = d.dpid
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
                AND d.name ILIKE %s ESCAPE ''
                AND pub.name ILIKE %s ESCAPE ''
                AND g.genre ILIKE %s ESCAPE ''
                AND vg_platform.price <= %s
                AND vg_platform.release_date >= %t
                AND vg_platform.release_date <= %t
            GROUP BY
                vg.Title, p.name, d.name, pub.name, vg_platform.price, vg_platform.release_date, vg.ESRB, ur.rating;
            """,("%"+title+"%","%"+platform+"%","%"+developer+"%","%"+publisher+"%","%"+genre+"%",int(price),releaseDateStart,releaseDateEnd))
        
        work = cur.fetchall()
        for i in work:
            print(i)
