def restart(ctx, copy, file, u):  # pylint:disable=redefined-builtin
    """Restart job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon job --job=1 restart
    ```
    """
    config = None
    update_code = None
    if file:
        config = rhea.read(file)

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)
        update_code = True

    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))
    try:
        if copy:
            response = PolyaxonClient().job.copy(
                user, project_name, _job, config=config, update_code=update_code)
        else:
            response = PolyaxonClient().job.restart(
                user, project_name, _job, config=config, update_code=update_code)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not restart job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    get_job_details(response)