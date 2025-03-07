import click

@click.group()
def follow():
    """Follow and unfollow users"""
    pass

@follow.command()
@click.argument('email', required=False)
def user(email):
    """Follow a user with an email
    
    \b
    Arguments:
        email   The user's email to follow
    """
    if not email:
        email = click.prompt('Enter email')
    click.echo(f'You\'re now following user with {email}')

@follow.command('unfollow')
@click.argument('email', required=False)
def unfollow_user(email):   
    """Unfollow a user with an email
    
    \b
    Arguments:
        email   The user's email to unfollow
    """
    if not email:
        email = click.prompt('Enter email')
    click.echo(f'You\'re now unfollowing user with {email}')
