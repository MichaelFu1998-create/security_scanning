def ci(ctx, enable, disable):  # pylint:disable=assign-to-new-keyword
    """Enable/Disable CI on this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon project ci --enable
    ```

    \b
    ```bash
    $ polyaxon project ci --disable
    ```
    """
    user, project_name = get_project_or_local(ctx.obj.get('project'))

    def enable_ci():
        try:
            PolyaxonClient().project.enable_ci(user, project_name)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not enable CI on project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        Printer.print_success(
            'Polyaxon CI was successfully enabled on project: `{}`.'.format(project_name))

    def disable_ci():
        try:
            PolyaxonClient().project.disable_ci(user, project_name)
        except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
            Printer.print_error('Could not disable CI on project `{}`.'.format(project_name))
            Printer.print_error('Error message `{}`.'.format(e))
            sys.exit(1)

        Printer.print_success(
            'Polyaxon CI was successfully disabled on project: `{}`.'.format(project_name))

    if enable:
        enable_ci()
    if disable:
        disable_ci()