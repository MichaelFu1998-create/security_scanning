def init(project, polyaxonfile):
    """Initialize a new polyaxonfile specification."""
    user, project_name = get_project_or_local(project)
    try:
        project_config = PolyaxonClient().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Make sure you have a project with this name `{}`'.format(project))
        Printer.print_error(
            'You can a create new project with this command: '
            'polyaxon project create '
            '--name={} [--description=...] [--tags=...]'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    init_project = False
    if ProjectManager.is_initialized():
        local_project = ProjectManager.get_config()
        click.echo('Warning! This project is already initialized with the following project:')
        with clint.textui.indent(4):
            clint.textui.puts('User: {}'.format(local_project.user))
            clint.textui.puts('Project: {}'.format(local_project.name))
        if click.confirm('Would you like to override this current config?', default=False):
            init_project = True
    else:
        init_project = True

    if init_project:
        ProjectManager.purge()
        ProjectManager.set_config(project_config, init=True)
        Printer.print_success('Project was initialized')
    else:
        Printer.print_header('Project config was not changed.')

    init_ignore = False
    if IgnoreManager.is_initialized():
        click.echo('Warning! Found a .polyaxonignore file.')
        if click.confirm('Would you like to override it?', default=False):
            init_ignore = True
    else:
        init_ignore = True

    if init_ignore:
        IgnoreManager.init_config()
        Printer.print_success('New .polyaxonignore file was created.')
    else:
        Printer.print_header('.polyaxonignore file was not changed.')

    if polyaxonfile:
        create_polyaxonfile()