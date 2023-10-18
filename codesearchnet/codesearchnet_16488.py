def stop(ctx, commit, yes):
    """Stops the notebook deployment for this project if it exists.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    if not yes and not click.confirm("Are sure you want to stop notebook "
                                     "for project `{}/{}`".format(user, project_name)):
        click.echo('Existing without stopping notebook.')
        sys.exit(1)

    if commit is None:
        commit = True

    try:
        PolyaxonClient().project.stop_notebook(user, project_name, commit)
        Printer.print_success('Notebook is being deleted')
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not stop notebook project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)