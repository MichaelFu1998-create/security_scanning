def create(name_or_path, config):
    '''Create a new environment.'''

    if not name_or_path:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        examples = (
            '\nExamples:\n'
            '    cpenv create my_env\n'
            '    cpenv create ./relative/path/to/my_env\n'
            '    cpenv create my_env --config ./relative/path/to/config\n'
            '    cpenv create my_env --config git@github.com:user/config.git\n'
        )
        click.echo(examples)
        return

    click.echo(
        blue('Creating a new virtual environment ' + name_or_path)
    )
    try:
        env = cpenv.create(name_or_path, config)
    except Exception as e:
        click.echo(bold_red('FAILED TO CREATE ENVIRONMENT!'))
        click.echo(e)
    else:
        click.echo(bold_green('Successfully created environment!'))
    click.echo(blue('Launching subshell'))

    cpenv.activate(env)
    shell.launch(env.name)