def add_cli_upload_bel(main: click.Group) -> click.Group:  # noqa: D202
    """Add several command to main :mod:`click` function related to export to BEL."""

    @main.command()
    @host_option
    @click.pass_obj
    def upload(manager: BELManagerMixin, host: str):
        """Upload BEL to BEL Commons."""
        graph = manager.to_bel()
        pybel.to_web(graph, host=host, public=True)

    return main