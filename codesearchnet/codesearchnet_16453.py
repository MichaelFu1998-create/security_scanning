def bookmark(ctx):
    """Bookmark build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build bookmark
    ```

    \b
    ```bash
    $ polyaxon build -b 2 bookmark
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        PolyaxonClient().build_job.bookmark(user, project_name, _build)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not bookmark build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build job bookmarked.")