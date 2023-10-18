def stop(ctx, yes):
    """Stops the tensorboard deployment for project/experiment/experiment group if it exists.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples: stopping project tensorboard

    \b
    ```bash
    $ polyaxon tensorboard stop
    ```

    Examples: stopping experiment group tensorboard

    \b
    ```bash
    $ polyaxon tensorboard -g 1 stop
    ```

    Examples: stopping experiment tensorboard

    \b
    ```bash
    $ polyaxon tensorboard -xp 112 stop
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    group = ctx.obj.get('group')
    experiment = ctx.obj.get('experiment')

    if experiment:
        obj = 'experiment `{}`'.format(experiment)
    elif group:
        obj = 'group `{}`'.format(group)
    else:
        obj = 'project `{}/{}`'.format(user, project_name)

    if not yes and not click.confirm("Are sure you want to stop tensorboard "
                                     "for {}".format(obj)):
        click.echo('Existing without stopping tensorboard.')
        sys.exit(1)

    if experiment:
        try:
            PolyaxonClient().experiment.stop_tensorboard(
                username=user,
                project_name=project_name,
                experiment_id=experiment)
            Printer.print_success('Tensorboard is being deleted')
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not stop tensorboard {}.'.format(obj))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    elif group:
        try:
            PolyaxonClient().experiment_group.stop_tensorboard(
                username=user,
                project_name=project_name,
                group_id=group)
            Printer.print_success('Tensorboard is being deleted')
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not stop tensorboard {}.'.format(obj))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)
    else:
        try:
            PolyaxonClient().project.stop_tensorboard(
                username=user,
                project_name=project_name)
            Printer.print_success('Tensorboard is being deleted')
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not stop tensorboard {}.'.format(obj))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)