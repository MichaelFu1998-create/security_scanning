def git(ctx, url, private, sync):  # pylint:disable=assign-to-new-keyword
    """Set/Sync git repo on this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon project git --url=https://github.com/polyaxon/polyaxon-quick-start
    ```

    \b
    ```bash
    $ polyaxon project git --url=https://github.com/polyaxon/polyaxon-quick-start --private
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    def git_set_url():
        if private:
            click.echo('\nSetting a private git repo "{}" on project: {} ...\n'.format(
                url, project_name))
        else:
            click.echo('\nSetting a public git repo "{}" on project: {} ...\n'.format(
                url, project_name))

        try:
            PolyaxonClient().project.set_repo(user, project_name, url, not private)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not set git repo on project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        Printer.print_success('Project was successfully initialized with `{}`.'.format(url))

    def git_sync_repo():
        try:
            response = PolyaxonClient().project.sync_repo(user, project_name)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not sync git repo on project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        click.echo(response.status_code)
        Printer.print_success('Project was successfully synced with latest changes.')

    if url:
        git_set_url()
    if sync:
        git_sync_repo()