def list(page):  # pylint:disable=redefined-builtin
    """List projects.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    user = AuthConfigManager.get_value('username')
    if not user:
        Printer.print_error('Please login first. `polyaxon login --help`')

    page = page or 1
    try:
        response = PolyaxonClient().project.list_projects(user, page=page)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get list of projects.')
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    meta = get_meta_response(response)
    if meta:
        Printer.print_header('Projects for current user')
        Printer.print_header('Navigation:')
        dict_tabulate(meta)
    else:
        Printer.print_header('No projects found for current user')

    objects = list_dicts_to_tabulate(
        [o.to_light_dict(
            humanize_values=True,
            exclude_attrs=['uuid', 'experiment_groups', 'experiments', 'description',
                           'num_experiments', 'num_independent_experiments',
                           'num_experiment_groups', 'num_jobs', 'num_builds', 'unique_name'])
            for o in response['results']])
    if objects:
        Printer.print_header("Projects:")
        dict_tabulate(objects, is_list_dict=True)