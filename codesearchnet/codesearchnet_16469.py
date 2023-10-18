def bookmark(ctx):
    """Bookmark group.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon group bookmark
    ```

    \b
    ```bash
    $ polyaxon group -g 2 bookmark
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj.get('project'),
                                                            ctx.obj.get('group'))

    try:
        PolyaxonClient().experiment_group.bookmark(user, project_name, _group)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not bookmark group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiments group is bookmarked.")