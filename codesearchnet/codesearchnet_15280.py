def get_cli(cls) -> click.Group:
        """Add  a :mod:`click` main function to use as a command line interface."""
        main = super().get_cli()

        cls._cli_add_flask(main)

        return main