def stop(ctx, yes, pending):
    """Stop experiments in the group.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples: stop only pending experiments

    \b
    ```bash
    $ polyaxon group stop --pending
    ```

    Examples: stop all unfinished

    \b
    ```bash
    $ polyaxon group stop
    ```

    \b
    ```bash
    $ polyaxon group -g 2 stop
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj.get('project'),
                                                            ctx.obj.get('group'))

    if not yes and not click.confirm("Are sure you want to stop experiments "
                                     "in group `{}`".format(_group)):
        click.echo('Existing without stopping experiments in group.')
        sys.exit(0)

    try:
        PolyaxonClient().experiment_group.stop(user, project_name, _group, pending=pending)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not stop experiments in group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiments in group are being stopped.")