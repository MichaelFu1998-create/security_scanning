def add_cli_clear_bel_namespace(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``clear_bel_namespace`` command to main :mod:`click` function."""

    @main.command()
    @click.pass_obj
    def drop(manager: BELNamespaceManagerMixin):
        """Clear names/identifiers to terminology store."""
        namespace = manager.drop_bel_namespace()

        if namespace:
            click.echo(f'namespace {namespace} was cleared')

    return main