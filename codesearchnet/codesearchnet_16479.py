def start(ctx, file):  # pylint:disable=redefined-builtin
    """Start a tensorboard deployment for project/experiment/experiment group.

    Project tensorboard will aggregate all experiments under the project.

    Experiment group tensorboard will aggregate all experiments under the group.

    Experiment tensorboard will show all metrics for an experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example: using the default tensorflow image 1.4.1.

    \b
    ```bash
    $ polyaxon tensorboard start
    ```

    Example: with custom image and resources

    \b
    ```bash
    $ polyaxon tensorboard start -f file -f file_override ...
    ```

    Example: starting a tensorboard for an experiment group

    \b
    ```bash
    $ polyaxon tensorboard -g 1 start -f file
    ```

    Example: starting a tensorboard for an experiment

    \b
    ```bash
    $ polyaxon tensorboard -xp 112 start -f file
    ```
    """
    specification = None
    job_config = None
    if file:
        specification = check_polyaxonfile(file, log=False).specification

    if specification:
        # pylint:disable=protected-access
        check_polyaxonfile_kind(specification=specification, kind=specification._TENSORBOARD)
        job_config = specification.parsed_data

    user, project_name = get_project_or_local(ctx.obj.get('project'))
    group = ctx.obj.get('group')
    experiment = ctx.obj.get('experiment')
    if experiment:
        try:
            response = PolyaxonClient().experiment.start_tensorboard(
                username=user,
                project_name=project_name,
                experiment_id=experiment,
                job_config=job_config)
            obj = 'experiment `{}`'.format(experiment)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not start tensorboard experiment `{}`.'.format(experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    elif group:
        try:
            response = PolyaxonClient().experiment_group.start_tensorboard(
                username=user,
                project_name=project_name,
                group_id=group,
                job_config=job_config)
            obj = 'group `{}`'.format(group)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not start tensorboard group `{}`.'.format(group))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    else:
        try:
            response = PolyaxonClient().project.start_tensorboard(
                username=user,
                project_name=project_name,
                job_config=job_config)
            obj = 'project `{}`'.format(project_name)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not start tensorboard project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    if response.status_code == 200:
        Printer.print_header("A tensorboard for this {} is already running on:".format(obj))
        click.echo(get_tensorboard_url(user=user,
                                       project_name=project_name,
                                       experiment=experiment,
                                       group=group))
        sys.exit(0)

    if response.status_code != 201:
        Printer.print_error('Something went wrong, Tensorboard was not created.')
        sys.exit(1)

    Printer.print_success('Tensorboard is being deployed for {}'.format(obj))
    clint.textui.puts("It may take some time before you can access tensorboard.\n")
    clint.textui.puts("Your tensorboard will be available on:\n")
    with clint.textui.indent(4):
        clint.textui.puts(get_tensorboard_url(user, project_name, experiment, group))