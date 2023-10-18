def update(ctx, name, description, tags):
    """Update build.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon build -b 2 update --description="new description for my build"
    ```
    """
    user, project_name, _build = get_build_or_local(ctx.obj.get('project'), ctx.obj.get('build'))
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    tags = validate_tags(tags)
    if tags:
        update_dict['tags'] = tags

    if not update_dict:
        Printer.print_warning('No argument was provided to update the build.')
        sys.exit(0)

    try:
        response = PolyaxonClient().build_job.update_build(
            user, project_name, _build, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not update build `{}`.'.format(_build))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Build updated.")
    get_build_details(response)