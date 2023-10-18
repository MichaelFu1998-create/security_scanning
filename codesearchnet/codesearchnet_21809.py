def add(name, path, branch, type):
    '''Add a module to an environment. PATH can be a git repository path or
    a filesystem path. '''

    if not name and not path:
        ctx = click.get_current_context()
        click.echo(ctx.get_help())
        examples = (
            '\nExamples:\n'
            '    cpenv module add my_module ./path/to/my_module\n'
            '    cpenv module add my_module git@github.com:user/my_module.git'
            '    cpenv module add my_module git@github.com:user/my_module.git --branch=master --type=shared'
        )
        click.echo(examples)
        return

    if not name:
        click.echo('Missing required argument: name')
        return

    if not path:
        click.echo('Missing required argument: path')

    env = cpenv.get_active_env()
    if type=='local':
        if not env:
            click.echo('\nActivate an environment to add a local module.\n')
            return

        if click.confirm('\nAdd {} to active env {}?'.format(name, env.name)):
            click.echo('Adding module...', nl=False)
            try:
                env.add_module(name, path, branch)
            except:
                click.echo(bold_red('FAILED'))
                raise
            else:
                click.echo(bold_green('OK!'))

        return

    module_paths = cpenv.get_module_paths()
    click.echo('\nAvailable module paths:\n')
    for i, mod_path in enumerate(module_paths):
        click.echo('    {}. {}'.format(i, mod_path))
    choice = click.prompt(
        'Where do you want to add your module?',
        type=int,
        default=0
    )
    module_root = module_paths[choice]
    module_path = utils.unipath(module_root, name)
    click.echo('Creating module {}...'.format(module_path), nl=False)
    try:
        cpenv.create_module(module_path, path, branch)
    except:
        click.echo(bold_red('FAILED'))
        raise
    else:
        click.echo(bold_green('OK!'))