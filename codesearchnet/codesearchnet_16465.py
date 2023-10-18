def get(ctx):
    """Get experiment group by uuid.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon group -g 13 get
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj.get('project'),
                                                            ctx.obj.get('group'))
    try:
        response = PolyaxonClient().experiment_group.get_experiment_group(
            user, project_name, _group)
        cache.cache(config_manager=GroupManager, response=response)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get experiment group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_group_details(response)