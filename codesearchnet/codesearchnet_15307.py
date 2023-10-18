def get_cli(cls) -> click.Group:
        """Get the :mod:`click` main function to use as a command line interface."""
        main = super().get_cli()

        cls._cli_add_populate(main)
        cls._cli_add_drop(main)
        cls._cli_add_cache(main)
        cls._cli_add_summarize(main)

        return main