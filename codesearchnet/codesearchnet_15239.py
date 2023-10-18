def add_cli_to_bel_namespace(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``upload_bel_namespace`` command to main :mod:`click` function."""

    @main.command()
    @click.option('-u', '--update', is_flag=True)
    @click.pass_obj
    def upload(manager: BELNamespaceManagerMixin, update):
        """Upload names/identifiers to terminology store."""
        namespace = manager.upload_bel_namespace(update=update)
        click.echo(f'uploaded [{namespace.id}] {namespace.keyword}')

    return main