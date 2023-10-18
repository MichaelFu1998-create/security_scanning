def list_():
    '''List available environments and modules'''

    click.echo('Cached Environments')

    environments = list(EnvironmentCache)
    click.echo(format_objects(environments, children=False))