import psycopg

def follow_user(conn: psycopg.Connection, args: list[str]):
    print(args)
    with conn.cursor() as cur:
        cur.execute(f"INSERT INTO follows (follower_uid, followee_uid) VALUES ('{args[0]}', '{args[1]}')")
        print("User followed")
    conn.commit()