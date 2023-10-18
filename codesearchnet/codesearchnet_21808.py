def create(name_or_path, config):
    '''Create a new template module.

    You can also specify a filesystem path like "./modules/new_module"
    '''

    click.echo('Creating module {}...'.format(name_or_path), nl=False)
    try:
        module = cpenv.create_module(name_or_path, config)
    except Exception as e:
        click.echo(bold_red('FAILED'))
        raise
    else:
        click.echo(bold_green('OK!'))
        click.echo('Browse to your new module and make some changes.')
        click.echo("When you're ready add the module to an environment:")
        click.echo('    cpenv module add my_module ./path/to/my_module')
        click.echo('Or track your module on git and add it directly from the repo:')
        click.echo('    cpenv module add my_module git@github.com:user/my_module.git')