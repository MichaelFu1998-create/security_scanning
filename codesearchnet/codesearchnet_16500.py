def groups(ctx, query, sort, page):
    """List experiment groups for this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    Get all groups:

    \b
    ```bash
    $ polyaxon project groups
    ```

    Get all groups with with status {created or running}, and
    creation date between 2018-01-01 and 2018-01-02,
    and search algorithm not in {grid or random search}

    \b
    ```bash
    $ polyaxon project groups \
      -q "status:created|running, started_at:2018-01-01..2018-01-02, search_algorithm:~grid|random"
    ```

    Get all groups sorted by update date

    \b
    ```bash
    $ polyaxon project groups -s "-updated_at"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    page = page or 1
    try:
        response = PolyaxonClient().project.list_experiment_groups(username=user,
                                                                   project_name=project_name,
                                                                   query=query,
                                                                   sort=sort,
                                                                   page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error(
            'Could not get experiment groups for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiment groups for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiment groups found for project `{}/{}`.'.format(
            user, project_name))

    objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
               for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiment groups:")
        objects.pop('project', None)
        objects.pop('user', None)
        dict_tabulate(objects, is_list_dict=True)