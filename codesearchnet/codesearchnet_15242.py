def add_cli_write_bel_annotation(main: click.Group) -> click.Group:  # noqa: D202
    """Add a ``write_bel_annotation`` command to main :mod:`click` function."""

    @main.command()
    @click.option('-d', '--directory', type=click.Path(file_okay=False, dir_okay=True), default=os.getcwd(),
                  help='output directory')
    @click.pass_obj
    def write(manager: BELNamespaceManagerMixin, directory: str):
        """Write a BEL annotation."""
        with open(os.path.join(directory, manager.identifiers_namespace), 'w') as file:
            manager.write_bel_annotation(file)

    return main