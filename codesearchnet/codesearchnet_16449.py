def get(ctx):
    """Get build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -b 1 get
    ```

    \b
    ```bash
    $ polyaxon build --build=1 --project=project_name get
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        response = PolyaxonClient().build_job.get_build(user, project_name, _build)
        cache.cache(config_manager=BuildJobManager, response=response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_build_details(response)