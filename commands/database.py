import click
import psycopg2
import os
from dotenv import load_dotenv
import sshtunnel as ssh
dotenv_path = '.env'
result = load_dotenv(dotenv_path)

@click.group()
@click.pass_context
def db(ctx):
    """Manage Postgres database"""
    if not result:
        raise click.ClickException(
       "❌ Missing .env file. Please create one with the following format:\n\n" \
       "        SSH_USER=your_ssh_username\n" \
       "        SSH_PASSWORD=your_ssh_password\n" \
       "        SSH_HOST=your_ssh_host\n" \
       "        DB_USER=your_db_username\n" \
       "        DB_PASSWORD=your_db_password\n" \
       "        DB_HOST=your_db_host\n" \
       "        DB_NAME=your_db_name\n" \
       "        DB_PORT=your_db_port")
    
    ssh_host = os.getenv('SSH_HOST')
    ssh_user = os.getenv('SSH_USER')
    ssh_password = os.getenv('SSH_PASSWORD')
    db_name = os.getenv('DB_NAME')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')

    with ssh.open_tunnel(
        (ssh_host, 22),  # SSH host and port
        ssh_username=ssh_user,
        ssh_password=ssh_password,  # Or use password authentication if needed
        remote_bind_address=(db_host, db_port)  # Remote database bind address and port
    ) as tunnel:
        try:
            conn = psycopg2.connect(
                database=db_name, 
                user=db_user, 
                password=db_password, 
                host=db_host,
                port=db_port,
                options="-c role=shp2382"
            )
            ctx.obj = conn

            click.echo("✅ Successfully connected to the database!")

            with conn.cursor() as cur:
                cur.execute("SELECT version();")
                version = cur.fetchone()
                click.echo(f"PostgreSQL version: {version[0]}")
            conn.close()

            return conn
        except psycopg2.Error as e:
            # print(tunnel)
            # print(db, db_user, db_password, db_host, db_port)
            raise click.ClickException(f"❌ Database connection failed: {e}")
        
@db.command("login")
@click.pass_context
def login(ctx):
    """Login to Postgres database"""
    conn = ctx.obj  # Retrieve connection from context
    click.echo(f"Using connection: {conn}")
    
db.add_command(login)


