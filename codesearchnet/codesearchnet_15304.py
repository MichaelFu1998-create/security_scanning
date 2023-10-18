def add_cli_summarize(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``summarize`` command to main :mod:`click` function."""

    @main.command()
    @click.pass_obj
    def summarize(manager: AbstractManager):
        """Summarize the contents of the database."""
        if not manager.is_populated():
            click.secho(f'{manager.module_name} has not been populated', fg='red')
            sys.exit(1)

        for name, count in sorted(manager.summarize().items()):
            click.echo(f'{name.capitalize()}: {count}')

    return main