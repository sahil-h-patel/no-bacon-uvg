import click

from commands.users import users
from commands.collections import collections
from commands.games import games
from commands.follow import follow

@click.group()
def cli():
    """No Bacon Unlimited Video Games - Video Game Collection Manager"""
    pass

# Register command groups
cli.add_command(users, name="user")
cli.add_command(collections, name="collection")
cli.add_command(games, name="game")
cli.add_command(follow)

if __name__ == "__main__":
    cli()
