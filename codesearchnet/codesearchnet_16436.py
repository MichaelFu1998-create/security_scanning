def get(ctx):
    """Get job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon job --job=1 get
    ```

    \b
    ```bash
    $ polyaxon job --job=1 --project=project_name get
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))
    try:
        response = PolyaxonClient().job.get_job(user, project_name, _job)
        cache.cache(config_manager=JobManager, response=response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_job_details(response)