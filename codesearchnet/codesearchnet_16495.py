def create(ctx, name, description, tags, private, init):
    """Create a new project.

    Uses [Caching](/references/polyaxon-cli/#caching)

    Example:

    \b
    ```bash
    $ polyaxon project create --name=cats-vs-dogs --description="Image Classification with DL"
    ```
    """
    try:
        tags = tags.split(',') if tags else None
        project_dict = dict(name=name, description=description, is_public=not private, tags=tags)
        project_config = ProjectConfig.from_dict(project_dict)
    except ValidationError:
        Printer.print_error('Project name should contain only alpha numerical, "-", and "_".')
        sys.exit(1)

    try:
        _project = PolyaxonClient().project.create_project(project_config)
    except (PolyaxonHTTPError, PolyaxonShouldExitError, PolyaxonClientException) as e:
        Printer.print_error('Could not create project `{}`.'.format(name))
        Printer.print_error('Error message `{}`.'.format(e))
        sys.exit(1)

    Printer.print_success("Project `{}` was created successfully.".format(_project.name))

    if init:
        ctx.obj = {}
        ctx.invoke(init_project, project=name)