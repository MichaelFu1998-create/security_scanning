def run(ctx, project, file, name, tags, description, ttl, u, l):  # pylint:disable=redefined-builtin
    """Run polyaxonfile specification.

    Examples:

    \b
    ```bash
    $ polyaxon run -f file -f file_override ...
    ```

    Upload before running

    \b
    ```bash
    $ polyaxon run -f file -u
    ```

    Run and set description and tags for this run

    \b
    ```bash
    $ polyaxon run -f file -u --description="Description of the current run" --tags="foo, bar, moo"
    ```
    Run and set a unique name for this run

    \b
    ```bash
    polyaxon run --name=foo
    ```

    Run for a specific project

    \b
    ```bash
    $ polyaxon run -p project1 -f file.yaml
    ```
    """
    if not file:
        file = PolyaxonFile.check_default_path(path='.')
    if not file:
        file = ''
    specification = check_polyaxonfile(file, log=False).specification

    spec_cond = (specification.is_experiment or
                 specification.is_group or
                 specification.is_job or
                 specification.is_build)
    if not spec_cond:
        Printer.print_error(
            'This command expects an experiment, a group, a job, or a build specification,'
            'received instead a `{}` specification'.format(specification.kind))
        if specification.is_notebook:
            click.echo('Please check "polyaxon notebook --help" to start a notebook.')
        elif specification.is_tensorboard:
            click.echo('Please check: "polyaxon tensorboard --help" to start a tensorboard.')
        sys.exit(1)

    # Check if we need to upload
    if u:
        if project:
            Printer.print_error('Uploading is not supported when switching project context!')
            click.echo('Please, either omit the `-u` option or `-p` / `--project=` option.')
            sys.exit(1)
        ctx.invoke(upload, sync=False)

    user, project_name = get_project_or_local(project)
    project_client = PolyaxonClient().project

    tags = validate_tags(tags)

    def run_experiment():
        click.echo('Creating an independent experiment.')
        experiment = ExperimentConfig(
            name=name,
            description=description,
            tags=tags,
            config=specification.parsed_data,
            ttl=ttl)
        try:
            response = PolyaxonClient().project.create_experiment(user,
                                                                  project_name,
                                                                  experiment)
            cache.cache(config_manager=ExperimentManager, response=response)
            Printer.print_success('Experiment `{}` was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create experiment.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_group():
        click.echo('Creating an experiment group with the following definition:')
        experiments_def = specification.experiments_def
        get_group_experiments_info(**experiments_def)
        experiment_group = ExperimentGroupConfig(
            name=name,
            description=description,
            tags=tags,
            content=specification._data)  # pylint:disable=protected-access
        try:
            response = project_client.create_experiment_group(user,
                                                              project_name,
                                                              experiment_group)
            cache.cache(config_manager=GroupManager, response=response)
            Printer.print_success('Experiment group {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create experiment group.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_job():
        click.echo('Creating a job.')
        job = JobConfig(
            name=name,
            description=description,
            tags=tags,
            config=specification.parsed_data,
            ttl=ttl)
        try:
            response = project_client.create_job(user,
                                                 project_name,
                                                 job)
            cache.cache(config_manager=JobManager, response=response)
            Printer.print_success('Job {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create job.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    def run_build():
        click.echo('Creating a build.')
        job = JobConfig(
            name=name,
            description=description,
            tags=tags,
            config=specification.parsed_data,
            ttl=ttl)
        try:
            response = project_client.create_build(user,
                                                   project_name,
                                                   job)
            cache.cache(config_manager=BuildJobManager, response=response)
            Printer.print_success('Build {} was created'.format(response.id))
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not create build.')
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    logs = None
    if specification.is_experiment:
        run_experiment()
        logs = experiment_logs
    elif specification.is_group:
        run_group()
    elif specification.is_job:
        run_job()
        logs = job_logs
    elif specification.is_build:
        run_build()
        logs = build_logs

    # Check if we need to invoke logs
    if l and logs:
        ctx.obj = {'project': '{}/{}'.format(user, project_name)}
        ctx.invoke(logs)