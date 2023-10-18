def download(ctx):
    """Download code of the current project."""
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    try:
        PolyaxonClient().project.download_repo(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not download code for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    Printer.print_success('Files downloaded.')