def statuses(ctx, job, page):
    """Get experiment or experiment job statuses.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples getting experiment statuses:

    \b
    ```bash
    $ polyaxon experiment statuses
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 statuses
    ```

    Examples getting experiment job statuses:

    \b
    ```bash
    $ polyaxon experiment statuses -j 3
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 statuses --job 1
    ```
    """

    def get_experiment_statuses():
        try:
            response = PolyaxonClient().experiment.get_statuses(
                user, project_name, _experiment, page=page)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could get status for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header('Statuses for experiment `{}`.'.format(_experiment))
            Printer.print_header('Navigation:')
            dict_tabulate(meta)
        else:
            Printer.print_header('No statuses found for experiment `{}`.'.format(_experiment))

        objects = list_dicts_to_tabulate(
            [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
             for o in response['results']])
        if objects:
            Printer.print_header("Statuses:")
            objects.pop('experiment', None)
            dict_tabulate(objects, is_list_dict=True)

    def get_experiment_job_statuses():
        try:
            response = PolyaxonClient().experiment_job.get_statuses(user,
                                                                    project_name,
                                                                    _experiment,
                                                                    _job,
                                                                    page=page)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get status for job `{}`.'.format(job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        meta = get_meta_response(response)
        if meta:
            Printer.print_header('Statuses for Job `{}`.'.format(_job))
            Printer.print_header('Navigation:')
            dict_tabulate(meta)
        else:
            Printer.print_header('No statuses found for job `{}`.'.format(_job))

        objects = list_dicts_to_tabulate(
            [Printer.add_status_color(o.to_light_dict(humanize_values=True), status_key='status')
             for o in response['results']])
        if objects:
            Printer.print_header("Statuses:")
            objects.pop('job', None)
            dict_tabulate(objects, is_list_dict=True)

    page = page or 1

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_statuses()
    else:
        get_experiment_statuses()