def remove(name_or_path):
    '''Remove an environment'''

    click.echo()
    try:
        r = cpenv.resolve(name_or_path)
    except cpenv.ResolveError as e:
        click.echo(e)
        return

    obj = r.resolved[0]
    if not isinstance(obj, cpenv.VirtualEnvironment):
        click.echo('{} is a module. Use `cpenv module remove` instead.')
        return

    click.echo(format_objects([obj]))
    click.echo()

    user_confirmed = click.confirm(
        red('Are you sure you want to remove this environment?')
    )
    if user_confirmed:
        click.echo('Attempting to remove...', nl=False)

        try:
            obj.remove()
        except Exception as e:
            click.echo(bold_red('FAIL'))
            click.echo(e)
        else:
            click.echo(bold_green('OK!'))