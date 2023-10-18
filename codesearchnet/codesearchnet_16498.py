def delete(ctx):
    """Delete project.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    if not click.confirm("Are sure you want to delete project `{}/{}`".format(user, project_name)):
        click.echo('Existing without deleting project.')
        sys.exit(1)

    try:
        response = PolyaxonClient().project.delete_project(user, project_name)
        local_project = ProjectManager.get_config()
        if local_project and (user, project_name) == (local_project.user, local_project.name):
            # Purge caching
            ProjectManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not delete project `{}/{}`.'.format(user, project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Project `{}/{}` was delete successfully".format(user, project_name))