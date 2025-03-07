import click

@click.group()
def users():
    """Manage users"""
    pass

@users.command('create')
@click.argument('username', required=False)
@click.argument('email', required=False)
def create_user(username, email):
    if not username and not email:
        username = click.prompt('Enter username')
        email = click.prompt('Enter email')
    print(f'User created with username: {username} and email: {email}')
