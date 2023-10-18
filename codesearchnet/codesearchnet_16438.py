def update(ctx, name, description, tags):
    """Update job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon job -j 2 update --description="new description for my job"
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))
    update_dict = {}

    if name:
        update_dict['name'] = name

    if description:
        update_dict['description'] = description

    tags = validate_tags(tags)
    if tags:
        update_dict['tags'] = tags

    if not update_dict:
        Printer.print_warning('No argument was provided to update the job.')
        sys.exit(0)

    try:
        response = PolyaxonClient().job.update_job(
            user, project_name, _job, update_dict)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not update job  `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Job updated.")
    get_job_details(response)