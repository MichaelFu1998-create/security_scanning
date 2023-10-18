def start(ctx, file, u):  # pylint:disable=redefined-builtin
    """Start a notebook deployment for this project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon notebook start -f file -f file_override ...
    ```

    Example: upload before running

    \b
    ```bash
    $ polyaxon -p user12/mnist notebook start -f file -u
    ```
    """
    specification = None
    job_config = None
    if file:
        specification = check_polyaxonfile(file, log=False).specification

    # Check if we need to upload
    if u:
        ctx.invoke(upload, sync=False)

    if specification:
        # pylint:disable=protected-access
        check_polyaxonfile_kind(specification=specification, kind=specification._NOTEBOOK)
        job_config = specification.parsed_data
    user, project_name = get_project_or_local(ctx.obj.get('project'))
    try:
        response = PolyaxonClient().project.start_notebook(user, project_name, job_config)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not start notebook project `{}`.'.format(project_name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    if response.status_code == 200:
        Printer.print_header("A notebook for this project is already running on:")
        click.echo(get_notebook_url(user, project_name))
        sys.exit(0)

    if response.status_code != 201:
        Printer.print_error('Something went wrong, Notebook was not created.')
        sys.exit(1)

    Printer.print_success('Notebook is being deployed for project `{}`'.format(project_name))
    clint.textui.puts("It may take some time before you can access the notebook.\n")
    clint.textui.puts("Your notebook will be available on:\n")
    with clint.textui.indent(4):
        clint.textui.puts(get_notebook_url(user, project_name))