def unbookmark(ctx):
    """Unbookmark experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment unbookmark
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 unbookmark
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    try:
        PolyaxonClient().experiment.unbookmark(user, project_name, _experiment)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not unbookmark experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment is unbookmarked.")