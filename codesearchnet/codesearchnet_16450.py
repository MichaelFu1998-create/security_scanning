def delete(ctx):
    """Delete build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon build delete
    ```

    \b
    ```bash
    $ polyaxon build -b 2 delete
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    if not click.confirm("Are sure you want to delete build job `{}`".format(_build)):
        click.echo('Existing without deleting build job.')
        sys.exit(1)

    try:
        response = PolyaxonClient().build_job.delete_build(
            user, project_name, _build)
        # Purge caching
        BuildJobManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not delete job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Build job `{}` was deleted successfully".format(_build))