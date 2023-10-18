def add(path):
    '''Add an environment to the cache. Allows you to activate the environment
    by name instead of by full path'''

    click.echo('\nAdding {} to cache......'.format(path), nl=False)
    try:
        r = cpenv.resolve(path)
    except Exception as e:
        click.echo(bold_red('FAILED'))
        click.echo(e)
        return

    if isinstance(r.resolved[0], cpenv.VirtualEnvironment):
        EnvironmentCache.add(r.resolved[0])
        EnvironmentCache.save()
        click.echo(bold_green('OK!'))