import click

@click.group()
def games():
    """Manage games in collections"""
    pass

@games.command('add')
@click.argument('game', required=False)
@click.argument('collection', required=False)
def add_game(game, collection):
    if not collection and not game:
        game = click.prompt('Enter game')
        collection = click.prompt('Enter collection')
    print(f'Added {game} to {collection}')

@games.command('delete')
@click.argument('game', required=False)
@click.argument('collection', required=False)
def delete_game(game, collection):
    if not collection and not game:
        game = click.prompt('Enter game')
        collection = click.prompt('Enter collection')
    print(f'Deleted {game} from {collection}')
