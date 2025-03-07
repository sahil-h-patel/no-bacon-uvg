import click

@click.group()
def cli():
    pass

@cli.command()
@click.argument('username', required=False)
@click.argument('email', required=False)
def create_user(username, email):
    if not username and not email:
        username = click.prompt('Enter username')
        email = click.prompt('Enter email')
        print(f'User created with username: {username} and email: {email}')
    elif username and email:
        print(f'User created with username: {username} and email: {email}')
    else:
        raise click.UsageError("Both username and email are required.")

@cli.command()
@click.argument('email', required=False)
def follow_user(email):
    if not email:
        email = click.prompt('Enter email')
    print(f'You\'re now following user with {email}')

@cli.command()
@click.argument('email', required=False)
def unfollow_user(email):
    if not email:
        email = click.prompt('Enter email')
    print(f'You\'re now unfollowing user with {email}')

@cli.command()
@click.argument('name', required=False)
def create_collection(name):
    if not name:
        name = click.prompt('Enter name')
    print(f'Successfully made collection with name {name}')

@cli.command()
@click.argument('name', required=False)
@click.argument('collection', required=False)
def rename_collection(name, collection):
    if not collection and not name:
        name = click.prompt('Enter name')
        collection = click.prompt('Enter collection')
        print(f'Renamed collection {collection} to {name}')
    elif collection and name:
        print(f'Renamed collection {collection} to {name}')
    else:
        raise click.UsageError("Both collection and name are required.")

@cli.command()
@click.argument('game', required=False)
@click.argument('collection', required=False)
def add_game(game, collection):
    # TODO: add warning when adding game to collection 
    #       for a platform that they don't own
    if not collection and not game:
        game = click.prompt('Enter game')
        collection = click.prompt('Enter collection')
        print(f'Added {game} to {collection}')
    elif collection and game:
        print(f'Added {game} to {collection}')
    else:
        raise click.UsageError("Both collection and game are required.")

@cli.command()
@click.argument('game', required=False)
@click.argument('collection', required=False)
def delete_game(game, collection):
    if not collection and not game:
        game = click.prompt('Enter game')
        collection = click.prompt('Enter collection')
        print(f'Deleted {game} to {collection}')
    elif collection and game:
        print(f'Deleted {game} to {collection}')
    else:
        raise click.UsageError("Both collection and game are required.")

@cli.command()
@click.argument('collection', required=False)
def delete_collection(collection):
    if not collection:
        collection = click.prompt('Enter collection')
    print(f'Successfully deleted {collection}')

def list_collection():
    pass
def search(**criteria):
    pass

''' 
    TODO: User search for video games by:
        - name
        - platform
        - release date
        - developer
        - price
        - genre
'''


