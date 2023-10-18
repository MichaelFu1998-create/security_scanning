def stop(ctx, yes):
    """Stop job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon job stop
    ```

    \b
    ```bash
    $ polyaxon job -xp 2 stop
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))
    if not yes and not click.confirm("Are sure you want to stop "
                                     "job `{}`".format(_job)):
        click.echo('Existing without stopping job.')
        sys.exit(0)

    try:
        PolyaxonClient().job.stop(user, project_name, _job)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not stop job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Job is being stopped.")