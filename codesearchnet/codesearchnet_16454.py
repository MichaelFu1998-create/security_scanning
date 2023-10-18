def resources(ctx, gpu):
    """Get build job resources.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build -b 2 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon build -b 2 resources --gpu
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    try:
        message_handler = Printer.gpu_resources if gpu else Printer.resources
        PolyaxonClient().build_job.resources(user,
                                             project_name,
                                             _build,
                                             message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get resources for build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)