def delete(ctx):
    """Delete experiment.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon experiment delete
    ```
    """
    user, project_name, _experiment = get_project_experiment_or_local(ctx.obj.get('project'),
                                                                      ctx.obj.get('experiment'))
    if not click.confirm("Are sure you want to delete experiment `{}`".format(_experiment)):
        click.echo('Existing without deleting experiment.')
        sys.exit(1)

    try:
        response = PolyaxonClient().experiment.delete_experiment(
            user, project_name, _experiment)
        # Purge caching
        ExperimentManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not delete experiment `{}`.'.format(_experiment))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment `{}` was delete successfully".format(_experiment))