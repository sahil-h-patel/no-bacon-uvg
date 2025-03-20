import psycopg

def example(conn: psycopg.Connection, args: list[str]):
    print(args)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        version = cur.fetchone()
        print(f'Rows:{version}')
