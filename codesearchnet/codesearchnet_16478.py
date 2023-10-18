def url(ctx):
    """Prints the tensorboard url for project/experiment/experiment group.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples for project tensorboards:

    \b
    ```bash
    $ polyaxon tensorboard url
    ```

    \b
    ```bash
    $ polyaxon tensorboard -p mnist url
    ```

    Examples for experiment tensorboards:

    \b
    ```bash
    $ polyaxon tensorboard -xp 1 url
    ```

    Examples for experiment group tensorboards:

    \b
    ```bash
    $ polyaxon tensorboard -g 1 url
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    group = ctx.obj.get('group')
    experiment = ctx.obj.get('experiment')
    if experiment:
        try:
            response = PolyaxonClient().experiment.get_experiment(
                username=user,
                project_name=project_name,
                experiment_id=experiment)
            obj = 'experiment {}'.format(experiment)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get experiment `{}`.'.format(experiment))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    elif group:
        try:
            response = PolyaxonClient().experiment_group.get_experiment_group(
                username=user,
                project_name=project_name,
                group_id=group)
            obj = 'group `{}`.'.format(group)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get group `{}`.'.format(group))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    else:
        try:
            response = PolyaxonClient().project.get_project(
                username=user,
                project_name=project_name)
            obj = 'project `{}`.'.format(project_name)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not get project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

    if response.has_tensorboard:
        click.echo(get_tensorboard_url(user=user,
                                       project_name=project_name,
                                       experiment=experiment,
                                       group=group))
    else:
        Printer.print_warning('This `{}` does not have a running tensorboard'.format(obj))
        click.echo('You can start tensorboard with this command: polyaxon tensorboard start --help')