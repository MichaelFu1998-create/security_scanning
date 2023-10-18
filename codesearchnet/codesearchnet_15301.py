def add_cli_populate(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``populate`` command to main :mod:`click` function."""

    @main.command()
    @click.option('--reset', is_flag=True, help='Nuke database first')
    @click.option('--force', is_flag=True, help='Force overwrite if already populated')
    @click.pass_obj
    def populate(manager: AbstractManager, reset, force):
        """Populate the database."""
        if reset:
            click.echo('Deleting the previous instance of the database')
            manager.drop_all()
            click.echo('Creating new models')
            manager.create_all()

        if manager.is_populated() and not force:
            click.echo('Database already populated. Use --force to overwrite')
            sys.exit(0)

        manager.populate()

    return main