def get(ctx):
    """Get info for current project, by project_name, or user/project_name.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    To get current project:

    \b
    ```bash
    $ polyaxon project get
    ```

    To get a project by name

    \b
    ```bash
    $ polyaxon project get user/project
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    try:
        response = PolyaxonClient().project.get_project(user, project_name)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_project_details(response)