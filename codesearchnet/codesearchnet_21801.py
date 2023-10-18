def list_():
    '''List available environments and modules'''

    environments = cpenv.get_environments()
    modules = cpenv.get_modules()
    click.echo(format_objects(environments + modules, children=True))