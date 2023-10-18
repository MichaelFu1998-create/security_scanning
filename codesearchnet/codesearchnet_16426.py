def restart(ctx, copy, file, u):  # pylint:disable=redefined-builtin
    """Restart experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Examples:

    \b
    ```bash
    $ polyaxon experiment --experiment=1 restart
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

    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    try:
        if copy:
            response = PolyaxonClient().experiment.copy(
                user, project_name, _experiment, config=config, update_code=update_code)
            Printer.print_success('Experiment was copied with id {}'.format(response.id))
        else:
            response = PolyaxonClient().experiment.restart(
                user, project_name, _experiment, config=config, update_code=update_code)
            Printer.print_success('Experiment was restarted with id {}'.format(response.id))
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not restart experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)