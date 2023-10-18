def update(ctx, name, description, tags):
    """Update experiment group.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon group -g 2 update --description="new description for this group"
    ```

    \b
    ```bash
    $ polyaxon update --tags="foo, bar"
    ```
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj.get('project'),
                                                            ctx.obj.get('group'))
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    tags = validate_tags(tags)
    if tags:
        update_dict['tags'] = tags

    if not update_dict:
        Printer.print_warning('No argument was provided to update the experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClient().experiment_group.update_experiment_group(
            user, project_name, _group, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not update experiment group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment group updated.")
    get_group_details(response)