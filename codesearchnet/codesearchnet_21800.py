def info():
    '''Show context info'''

    env = cpenv.get_active_env()
    modules = []
    if env:
        modules = env.get_modules()
    active_modules = cpenv.get_active_modules()

    if not env and not modules and not active_modules:
        click.echo('\nNo active modules...')
        return

    click.echo(bold('\nActive modules'))
    if env:
        click.echo(format_objects([env] + active_modules))

        available_modules = set(modules) - set(active_modules)
        if available_modules:

            click.echo(
                bold('\nInactive modules in {}\n').format(cyan(env.name))
            )
            click.echo(format_objects(available_modules, header=False))

    else:
        click.echo(format_objects(active_modules))

    available_shared_modules = set(cpenv.get_modules()) - set(active_modules)
    if not available_shared_modules:
        return

    click.echo(bold('\nInactive shared modules \n'))
    click.echo(format_objects(available_shared_modules, header=False))