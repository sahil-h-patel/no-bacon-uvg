import click

@click.group()
def users():
    """Manage users"""
    pass

@users.command('create')
@click.argument('username', required=False)
@click.argument('email', required=False)
def create_user(username, email):
    """Create a new user in the database
    
    \b
    Arguments:
        username    The username for the new user
        email       The email for the new user
    """
    if not username and not email:
        username = click.prompt('Enter username')
        email = click.prompt('Enter email')
    click.echo(f'User created with username: {username} and email: {email}')
