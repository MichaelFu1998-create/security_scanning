def logs(ctx, job, past, follow, hide_time):
    """Get experiment or experiment job logs.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting experiment logs:

    \b
    ```bash
    $ polyaxon experiment logs
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 10 -p mnist logs
    ```

    Examples for getting experiment job logs:

    \b
    ```bash
    $ polyaxon experiment -xp 1 -j 1 logs
    ```
    """

    def get_experiment_logs():
        if past:
            try:
                response = PolyaxonClient().experiment.logs(
                    user, project_name, _experiment, stream=False)
                get_logs_handler(handle_job_info=True,
                                 show_timestamp=not hide_time,
                                 stream=False)(response.content.decode().split('\n'))
                print()

                if not follow:
                    return
            except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
                if not follow:
                    Printer.print_error(
                        'Could not get logs for experiment `{}`.'.format(_experiment))
                    Printer.print_error(
                        'Error message `{}`.'.format(e))
                    sys.exit(1)

        try:
            PolyaxonClient().experiment.logs(
                user,
                project_name,
                _experiment,
                message_handler=get_logs_handler(handle_job_info=True,
                                                 show_timestamp=not hide_time))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get logs for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def get_experiment_job_logs():
        if past:
            try:
                response = PolyaxonClient().experiment_job.logs(
                    user,
                    project_name,
                    _experiment,
                    _job,
                    stream=False)
                get_logs_handler(handle_job_info=True,
                                 show_timestamp=not hide_time,
                                 stream=False)(response.content.decode().split('\n'))
                print()

                if not follow:
                    return
            except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
                if not follow:
                    Printer.print_error(
                        'Could not get logs for experiment `{}`.'.format(_experiment))
                    Printer.print_error(
                        'Error message `{}`.'.format(e))
                    sys.exit(1)

        try:
            PolyaxonClient().experiment_job.logs(
                user,
                project_name,
                _experiment,
                _job,
                message_handler=get_logs_handler(handle_job_info=True,
                                                 show_timestamp=not hide_time))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get logs for job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_logs()
    else:
        get_experiment_logs()