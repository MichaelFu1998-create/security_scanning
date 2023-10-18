def delete(ctx):
    """Delete experiment group.

    Uses [Caching](/references/polyaxon-cli/#caching)
    """
    user, project_name, _group = get_project_group_or_local(ctx.obj.get('project'),
                                                            ctx.obj.get('group'))

    if not click.confirm("Are sure you want to delete experiment group `{}`".format(_group)):
        click.echo('Existing without deleting experiment group.')
        sys.exit(0)

    try:
        response = PolyaxonClient().experiment_group.delete_experiment_group(
            user, project_name, _group)
        # Purge caching
        GroupManager.purge()
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not delete experiment group `{}`.'.format(_group))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 204:
        Printer.print_success("Experiment group `{}` was delete successfully".format(_group))