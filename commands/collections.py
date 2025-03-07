import click

@click.group()
def collections():
    """Manage game collections"""
    pass

@collections.command('create')
@click.argument('name', required=False)
def create_collection(name):
    if not name:
        name = click.prompt('Enter name')
    print(f'Successfully made collection with name {name}')

@collections.command('delete')
@click.argument('name', required=False)
def delete_collection(name):
    if not name:
        name = click.prompt('Enter collection')
    print(f'Successfully deleted {name}')

@collections.command('rename')
@click.argument('name', required=False)
@click.argument('collection', required=False)
def rename_collection(name, collection):
    if not collection and not name:
        name = click.prompt('Enter new name')
        collection = click.prompt('Enter collection to rename')
    print(f'Renamed collection {collection} to {name}')
