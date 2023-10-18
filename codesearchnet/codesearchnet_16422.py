def get(ctx, job):
    """Get experiment or experiment job.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for getting an experiment:

    \b
    ```bash
    $ polyaxon experiment get  # if experiment is cached
    ```

    \b
    ```bash
    $ polyaxon experiment --experiment=1 get
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 --project=cats-vs-dogs get
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get
    ```

    Examples for getting an experiment job:

    \b
    ```bash
    $ polyaxon experiment get -j 1  # if experiment is cached
    ```

    \b
    ```bash
    $ polyaxon experiment --experiment=1 get --job=10
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 --project=cats-vs-dogs get -j 2
    ```

    \b
    ```bash
    $ polyaxon experiment -xp 1 -p alain/cats-vs-dogs get -j 2
    ```
    """

    def get_experiment():
        try:
            response = PolyaxonClient().experiment.get_experiment(user, project_name, _experiment)
            cache.cache(config_manager=ExperimentManager, response=response)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not load experiment `{}` info.'.format(_experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        get_experiment_details(response)

    def get_experiment_job():
        try:
            response = PolyaxonClient().experiment_job.get_job(user,
                                                               project_name,
                                                               _experiment,
                                                               _job)
            cache.cache(config_manager=ExperimentJobManager, response=response)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get job `{}`.'.format(_job))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        if response.resources:
            get_resources(response.resources.to_dict(), header="Job resources:")

        response = Printer.add_status_color(response.to_light_dict(
            humanize_values=True,
            exclude_attrs=['uuid', 'definition', 'experiment', 'unique_name', 'resources']
        ))
        Printer.print_header("Job info:")
        dict_tabulate(response)

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))

    if job:
        _job = get_experiment_job_or_local(job)
        get_experiment_job()
    else:
        get_experiment()