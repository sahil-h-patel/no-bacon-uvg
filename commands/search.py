import psycopg
from typing import Any, Callable
from datetime import datetime, date

from psycopg.abc import Params
from psycopg.rows import TupleRow

DATE_FORMAT = "%m-%d-%Y"
COLUMNS = ("vid", "title", "pid", "platform", "release_date", "video_game_developer_name", "video_game_publisher_name", "esrb", "price", "genre", "playtime", "rating")

def _search_with_condition(conn: psycopg.Connection, condition: str, params: Params):
    with conn.cursor() as cur:
        cur.execute(
            f'''
                SELECT
                    vg.vid,
                    vg.title,
                    p.pid,
                    p.name as platform,
                    vgpf.release_date,
                    vgd.name as video_game_developer_name,
                    vgpb.name as video_game_publisher_name,
                    vg.esrb,
                    vgpf.price,
                    g.genre,
                    SUM(up.end_time - up.start_time) as playtime,
                    AVG(ur.rating) as rating
                FROM video_games vg
                        LEFT JOIN video_game_platforms vgpf ON vg.vid = vgpf.vid
                        LEFT JOIN platform p ON vgpf.pid = p.pid
                        LEFT JOIN (SELECT * FROM video_game_developer _vgd LEFT JOIN contributor ON _vgd.dpid = contributor.dpid) vgd ON vg.vid = vgd.vid
                        LEFT JOIN (SELECT * FROM video_game_publisher _vgpb LEFT JOIN contributor ON _vgpb.dpid = contributor.dpid) vgpb ON vg.vid = vgpb.vid
                        LEFT JOIN user_plays up ON (vg.vid = up.vid)
                        LEFT JOIN user_rating ur ON (vg.vid = ur.vid)
                        LEFT JOIN video_game_genre vgg ON vg.vid = vgg.vid
                        LEFT JOIN genre g ON vgg.gid = g.gid
                {condition}
                GROUP BY vg.vid, vg.title, p.name, vgd.name, vgpb.name, vgpf.release_date, vgpf.price, g.genre, p.pid
                ORDER BY vg.title, vgpf.release_date
            ''', # type: ignore
            params
        )
        return cur.fetchall()

def search_title(conn: psycopg.Connection, args: list[str]):
    if len(args) != 1:
        print("usage: search title [title]")
        return
    return _search_with_condition(conn, "WHERE vg.title ILIKE %s", (f"%{args[0]}%",)),

def search_platform(conn: psycopg.Connection, args: list[str]):
    if len(args) != 1:
        print("usage: search platform [platform]")
        return
    return _search_with_condition(conn, "WHERE p.name ILIKE %s", (f"%{args[0]}%",)),

def search_release_date(conn: psycopg.Connection, args: list[str]):
    if len(args) != 2:
        print(f"usage: search release_date [start_date] [end_date] (format: {DATE_FORMAT})")
        return
    start_date = args[0]
    try:
        start_date = datetime.strptime(start_date, DATE_FORMAT)
    except:
        print("invalid date, exiting")
        return
    end_date = args[1]
    try:
        end_date = datetime.strptime(end_date, DATE_FORMAT)
    except:
        print("invalid date, exiting")
        return
    return _search_with_condition(conn, "WHERE vgpf.release_date >= %s AND vgpf.release_date <= %s", (start_date,end_date)),

def search_developer(conn: psycopg.Connection, args: list[str]):
    if len(args) != 1:
        print("usage: search developer [developer]")
        return
    return _search_with_condition(conn, "WHERE vgd.name ILIKE %s", (f"%{args[0]}%",)),

def search_publisher(conn: psycopg.Connection, args: list[str]):
    if len(args) != 1:
        print("usage: search publisher [publisher]")
        return
    return _search_with_condition(conn, "WHERE vgpb.name ILIKE %s", (f"%{args[0]}%",)),

def search_price(conn: psycopg.Connection, args: list[str]):
    if len(args) != 2:
        print("usage: search price [min_price] [max_price]")
        return

    try:
        min_price = int(args[0])
    except:
        print("invalid min_price")
        return

    try:
        max_price = int(args[1])
    except:
        print("invalid max_price")
        return

    return _search_with_condition(conn, "WHERE vgpf.price >= %s AND vgpf.price <= %s", (min_price, max_price)),

def search_genre(conn: psycopg.Connection, args: list[str]):
    if len(args) != 1:
        print("usage: search genre [genre]")
        return
    return _search_with_condition(conn, "WHERE g.genre ILIKE %s", (f"%{args[0]}%",)),


ARGS = {
    "title": search_title,
    "platform": search_platform,
    "release_date": search_release_date,
    "developer": search_developer,
    "publisher": search_publisher,
    "price": search_price,
    "genre": search_genre
}

def row_to_dict(row: TupleRow) -> dict[str, Any]:
    dict = {}
    for i in range(len(row)):
        dict[COLUMNS[i]] = row[i]
    return dict

def print_data(data: list[TupleRow], sort_func: Callable[[Any], Any], decending: bool):
    games = {}
    for row in map(row_to_dict, data):
        vid = row["vid"]
        if vid not in games:
            games[vid] = {
                "title": row["title"],
                "esrb": row["esrb"],
                "playtime": row["playtime"],
                "rating": row["rating"],
                "platforms": {},
                "publishers": set(),
                "developers": set(),
                "genre": row["genre"]
            }
        games[vid]["developers"].add(row["video_game_developer_name"])
        games[vid]["publishers"].add(row["video_game_publisher_name"])

        pid = row["pid"]

        if pid not in games[vid]["platforms"]:
            games[vid]["platforms"][pid] = {
                "name": row["platform"],
                "price": row["price"],
                "release_date": row["release_date"]
            }

    sorted_games = sorted(games.values(), key=sort_func, reverse=decending)

    for game in sorted_games:
        print(f"{game["title"]} - {game["rating"]:.2f} Stars - Playtime: {game["playtime"]} - ESRB: {game["esrb"]} - Genre: {game["genre"]}")
        print(f"\tPublishers - {", ".join(game["publishers"])}")
        print(f"\tDevelopers - {", ".join(game["developers"])}")
        print( "\tPlatforms Released On:")
        for platform in game["platforms"].values():
            print(f"\t\t{platform["name"]} - ${platform["price"]} on {platform["release_date"]}")


def sort_title(d):
    return d['title']

def sort_min_price(d):
    min = 99999999
    for p in d["platforms"].values():
        if min > p["price"]:
            min = p["price"]
    return min

def sort_max_price(d):
    max = 0
    for p in d["platforms"].values():
        if max < p["price"]:
            max = p["price"]
    return max

def sort_genre(d):
    return d['genre']

def sort_min_release_date(d):
    min = date.max
    for p in d["platforms"].values():
        if min > p["release_date"]:
            min = p["release_date"]
    return min
def sort_max_release_date(d):
    max = date.min
    for p in d["platforms"].values():
        if max < p["release_date"]:
            max = p["release_date"]
    return max

def search(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    if len(args) == 0 or args[0] not in ARGS:
        print(f"search [{"|".join(ARGS.keys())}]")
        return
    data = ARGS[args[0]](conn, args[1::])

    if not data:
        return

    data = data[0]

    print_data(data, sort_title, False)
    while True:
        try:
            cmd = input("Sort by (t)itle/(p/P)rice/(g)enre/(r/R)elease date (a)scending/(d)ecending\n[tpgre][ad]: ")
        except:
            print("Failed to get input. Exiting search mode...")
            return

        if len(cmd) != 2:
            print("Impropper format.")
            continue

        is_dec = (cmd[1] == 'd')

        match cmd[0]:
            case 't':
                print_data(data, sort_title, is_dec)
            case 'p':
                print_data(data, sort_min_price, is_dec)
            case 'P':
                print_data(data, sort_max_price, is_dec)
            case 'g':
                print_data(data, sort_genre, is_dec)
            case 'r':
                print_data(data, sort_min_release_date, is_dec)
            case 'R':
                print_data(data, sort_max_release_date, is_dec)
            case 'e':
                break
