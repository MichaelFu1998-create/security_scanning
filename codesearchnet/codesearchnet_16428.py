def resources(ctx, job, gpu):
    """Get experiment or experiment job resources.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting experiment resources:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources --gpu
    ```

    Examples for getting experiment job resources:

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources -j 1
    ```

    For GPU resources

    \b
    ```bash
    $ polyaxon experiment -xp 19 resources -j 1 --gpu
    ```
    """

    def get_experiment_resources():
        try:
            message_handler = Printer.gpu_resources if gpu else Printer.resources
            PolyaxonClient().experiment.resources(
                user, project_name, _experiment, message_handler=message_handler)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get resources for experiment `{}`.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def get_experiment_job_resources():
        try:
            message_handler = Printer.gpu_resources if gpu else Printer.resources
            PolyaxonClient().experiment_job.resources(user,
                                                      project_name,
                                                      _experiment,
                                                      _job,
                                                      message_handler=message_handler)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get resources for job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job_resources()
    else:
        get_experiment_resources()