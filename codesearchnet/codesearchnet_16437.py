def delete(ctx):
    """Delete job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon job delete
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))
    if not click.confirm("Are sure you want to delete job `{}`".format(_job)):
        click.echo('Existing without deleting job.')
        sys.exit(1)

    try:
        response = PolyaxonClient().job.delete_job(
            user, project_name, _job)
        # Purge caching
        JobManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not delete job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Job `{}` was delete successfully".format(_job))