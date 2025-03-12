import click

@click.group()
def collections():
    """Manage game collections"""
    pass

@collections.command('create')
@click.argument('name', required=False)
def create_collection(name):
    """Create a new game collection.

    \b
    Arguments:
      name  The name of the collection to create.
    """
    if not name:
        name = click.prompt('Enter name')
    click.echo(f'Successfully made collection with name {name}')

@collections.command('delete')
@click.argument('name', required=False)
def delete_collection(name):
    """Delete an existing game collection.

    \b
    Arguments:
      name  The name of the collection to delete.
    """
    if not name:
        name = click.prompt('Enter collection')
    click.echo(f'Successfully deleted {name}')

@collections.command('rename')
@click.argument('name', required=False)
@click.argument('collection', required=False)
def rename_collection(name, collection):
    """Rename a game collection.

    \b
    Arguments:
      old_name  The current name of the collection.
      new_name  The new name for the collection.
    """
    if not name and not collection:
        name = click.prompt('Enter new name')
        collection = click.prompt('Enter collection to rename')
    elif name and not collection:
        raise click.UsageError("Please use both arguments, name and collection")
    click.echo(f'Renamed collection {collection} to {name}')
