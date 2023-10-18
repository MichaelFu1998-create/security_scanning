def localize(name):
    '''Copy a global module to the active environment.'''

    env = cpenv.get_active_env()
    if not env:
        click.echo('You need to activate an environment first.')
        return

    try:
        r = cpenv.resolve(name)
    except cpenv.ResolveError as e:
        click.echo('\n' + str(e))

    module = r.resolved[0]
    if isinstance(module, cpenv.VirtualEnvironment):
        click.echo('\nCan only localize a module not an environment')
        return

    active_modules = cpenv.get_active_modules()
    if module in active_modules:
        click.echo('\nCan not localize an active module.')
        return

    if module in env.get_modules():
        click.echo('\n{} is already local to {}'.format(module.name, env.name))
        return

    if click.confirm('\nAdd {} to env {}?'.format(module.name, env.name)):
        click.echo('Adding module...', nl=False)
        try:
            module = env.add_module(module.name, module.path)
        except:
            click.echo(bold_red('FAILED'))
            raise
        else:
            click.echo(bold_green('OK!'))

    click.echo('\nActivate the localize module:')
    click.echo('    cpenv activate {} {}'.format(env.name, module.name))