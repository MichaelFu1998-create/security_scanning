def outputs(ctx):
    """Download outputs for job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon job -j 1 outputs
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))
    try:
        PolyaxonClient().job.download_outputs(user, project_name, _job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not download outputs for job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)
    Printer.print_success('Files downloaded.')