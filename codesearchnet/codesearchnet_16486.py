def url(ctx):
    """Prints the notebook url for this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon notebook url
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    try:
        response = PolyaxonClient().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.has_notebook:
        click.echo(get_notebook_url(user, project_name))
    else:
        Printer.print_warning(
            'This project `{}` does not have a running notebook.'.format(project_name))
        click.echo('You can start a notebook with this command: polyaxon notebook start --help')