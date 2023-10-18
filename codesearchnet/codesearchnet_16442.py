def resources(ctx, gpu):
    """Get job resources.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon job -j 2 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon job -j 2 resources --gpu
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))
    try:
        message_handler = Printer.gpu_resources if gpu else Printer.resources
        PolyaxonClient().job.resources(user,
                                       project_name,
                                       _job,
                                       message_handler=message_handler)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get resources for job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)