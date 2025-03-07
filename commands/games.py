import click

@click.group()
def games():
    """Manage games in collections"""
    pass

@games.command('add')
@click.argument('game', required=False)
@click.argument('collection', required=False)
def add_game(game, collection):
    """Add a game to a collection
    
    \b
    Arguments:
        game          The game to add
        collection    The collection the game will be added to
    """
    if not collection and not game:
        game = click.prompt('Enter game')
        collection = click.prompt('Enter collection')
    click.echo(f'Added {game} to {collection}')

@games.command('delete')
@click.argument('game', required=False)
@click.argument('collection', required=False)
def delete_game(game, collection):
    """Delete a game to a collection
    
    \b
    Arguments:
        game          The game to delete
        collection    The collection the game will be deleted from
    """
    if not collection and not game:
        game = click.prompt('Enter game')
        collection = click.prompt('Enter collection')
    click.echo(f'Deleted {game} from {collection}')
