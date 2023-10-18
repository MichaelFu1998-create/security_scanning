def logs(ctx, past, follow, hide_time):
    """Get job logs.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon job -j 2 logs
    ```

    \b
    ```bash
    $ polyaxon job logs
    ```
    """
    user, project_name, _job = get_job_or_local(ctx.obj.get('project'), ctx.obj.get('job'))

    if past:
        try:
            response = PolyaxonClient().job.logs(
                user, project_name, _job, stream=False)
            get_logs_handler(handle_job_info=False,
                             show_timestamp=not hide_time,
                             stream=False)(response.content.decode().split('\n'))
            print()

            if not follow:
                return
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            if not follow:
                Printer.print_error('Could not get logs for job `{}`.'.format(_job))
                Printer.print_error('Error message `{}`.'.format(e))
                sys.exit(1)

    try:
        PolyaxonClient().job.logs(
            user,
            project_name,
            _job,
            message_handler=get_logs_handler(handle_job_info=False, show_timestamp=not hide_time))
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not get logs for job `{}`.'.format(_job))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)