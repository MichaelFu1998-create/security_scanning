def add_cli_write_bel_namespace(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``write_bel_namespace`` command to main :mod:`click` function."""

    @main.command()
    @click.option('-d', '--directory', type=click.Path(file_okay=False, dir_okay=True), default=os.getcwd(),
                  help='output directory')
    @click.pass_obj
    def write(manager: BELNamespaceManagerMixin, directory: str):
        """Write a BEL namespace names/identifiers to terminology store."""
        manager.write_directory(directory)

    return main