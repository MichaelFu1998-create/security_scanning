def get_cli(cls) -> click.Group:
        """Get a :mod:`click` main function with added BEL namespace commands."""
        main = super().get_cli()

        if cls.is_namespace:
            @main.group()
            def belns():
                """Manage BEL namespace."""

            cls._cli_add_to_bel_namespace(belns)
            cls._cli_add_clear_bel_namespace(belns)
            cls._cli_add_write_bel_namespace(belns)

        if cls.is_annotation:
            @main.group()
            def belanno():
                """Manage BEL annotation."""

            cls._cli_add_write_bel_annotation(belanno)

        return main