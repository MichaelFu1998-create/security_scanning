def add_cli_drop(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``drop`` command to main :mod:`click` function."""

    @main.command()
    @click.confirmation_option(prompt='Are you sure you want to drop the db?')
    @click.pass_obj
    def drop(manager):
        """Drop the database."""
        manager.drop_all()

    return main