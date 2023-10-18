def stop(ctx, yes):
    """Stop build job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon build stop
    ```

    \b
    ```bash
    $ polyaxon build -b 2 stop
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    if not yes and not click.confirm("Are sure you want to stop "
                                     "job `{}`".format(_build)):
        click.echo('Existing without stopping build job.')
        sys.exit(0)

    try:
        PolyaxonClient().build_job.stop(user, project_name, _build)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not stop build job `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build job is being stopped.")