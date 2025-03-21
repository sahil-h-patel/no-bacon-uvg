import psycopg
from typing import Any

def search(conn: psycopg.Connection, args: list[str], ctx: dict[str, Any]):
    print("pretty sure, yeah")