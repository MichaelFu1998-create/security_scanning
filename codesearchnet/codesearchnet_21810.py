def remove(name, local):
    '''Remove a module named NAME. Will remove the first resolved module named NAME. You can also specify a full path to a module. Use the --local option
    to ensure removal of modules local to the currently active environment.'''

    click.echo()
    if not local: # Use resolver to find module
        try:
            r = cpenv.resolve(name)
        except cpenv.ResolveError as e:
            click.echo(e)
            return

        obj = r.resolved[0]
    else: # Try to find module in active environment
        env = cpenv.get_active_env()
        if not env:
            click.echo('You must activate an env to remove local modules')
            return

        mod = env.get_module(name)
        if not mod:
            click.echo('Failed to resolve module: ' + name)
            return

        obj = mod

    if isinstance(obj, cpenv.VirtualEnvironment):
        click.echo('{} is an environment. Use `cpenv remove` instead.')
        return

    click.echo(format_objects([obj]))
    click.echo()

    user_confirmed = click.confirm(
        red('Are you sure you want to remove this module?')
    )
    if user_confirmed:
        click.echo('Attempting to remove...', nl=False)

        try:
            obj.remove()
        except Exception as e:
            click.echo(bold_red('FAILED'))
            click.echo(e)
        else:
            click.echo(bold_green('OK!'))