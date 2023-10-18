def update(ctx, name, description, tags):
    """Update experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment -xp 2 update --description="new description for my experiments"
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 2 update --tags="foo, bar" --name="unique-name"
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    tags = validate_tags(tags)
    if tags:
        update_dict['tags'] = tags

    if not update_dict:
        Printer.print_warning('No argument was provided to update the experiment.')
        sys.exit(0)

    try:
        response = PolyaxonClient().experiment.update_experiment(
            user, project_name, _experiment, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not update experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Experiment updated.")
    get_experiment_details(response)