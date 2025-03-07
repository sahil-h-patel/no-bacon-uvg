import click

@click.group()
def follow():
    """Follow and unfollow users"""
    pass

@follow.command()
@click.argument('email', required=False)
def user(email):
    if not email:
        email = click.prompt('Enter email')
    print(f'You\'re now following user with {email}')

@follow.command('unfollow')
@click.argument('email', required=False)
def unfollow_user(email):
    if not email:
        email = click.prompt('Enter email')
    print(f'You\'re now unfollowing user with {email}')
