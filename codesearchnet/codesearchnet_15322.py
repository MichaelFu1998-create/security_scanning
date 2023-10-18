def add_cli_to_bel(main: click.Group) -> click.Group:  # noqa: D202
    """Add several command to main :mod:`click` function related to export to BEL."""

    @main.command()
    @click.option('-o', '--output', type=click.File('w'), default=sys.stdout)
    @click.option('-f', '--fmt', default='bel', show_default=True, help='BEL export format')
    @click.pass_obj
    def write(manager: BELManagerMixin, output: TextIO, fmt: str):
        """Write as BEL Script."""
        graph = manager.to_bel()
        graph.serialize(file=output, fmt=fmt)
        click.echo(graph.summary_str())

    return main