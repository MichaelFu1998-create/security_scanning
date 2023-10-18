def experiments(ctx, metrics, declarations, independent, group, query, sort, page):
    """List experiments for this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    Get all experiments:

    \b
    ```bash
    $ polyaxon project experiments
    ```

    Get all experiments with with status {created or running}, and
    creation date between 2018-01-01 and 2018-01-02, and declarations activation equal to sigmoid
    and metric loss less or equal to 0.2

    \b
    ```bash
    $ polyaxon project experiments \
      -q "status:created|running, started_at:2018-01-01..2018-01-02, \
          declarations.activation:sigmoid, metric.loss:<=0.2"
    ```

    Get all experiments sorted by update date

    \b
    ```bash
    $ polyaxon project experiments -s "-updated_at"
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    page = page or 1
    try:
        response = PolyaxonClient().project.list_experiments(username=user,
                                                             project_name=project_name,
                                                             independent=independent,
                                                             group=group,
                                                             metrics=metrics,
                                                             declarations=declarations,
                                                             query=query,
                                                             sort=sort,
                                                             page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get experiments for project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Experiments for project `{}/{}`.'.format(user, project_name))
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No experiments found for project `{}/{}`.'.format(user, project_name))

    if metrics:
        objects = get_experiments_with_metrics(response)
    elif declarations:
        objects = get_experiments_with_declarations(response)
    else:
        objects = [Printer.add_status_color(o.to_light_dict(humanize_values=True))
                   for o in response['results']]
    objects = list_dicts_to_tabulate(objects)
    if objects:
        Printer.print_header("Experiments:")
        objects.pop('project_name', None)
        dict_tabulate(objects, is_list_dict=True)