def get_cli(cls) -> click.Group:
        """Get a :mod:`click` main function with added BEL commands."""
        main = super().get_cli()

        @main.group()
        def bel():
            """Manage BEL."""

        cls._cli_add_to_bel(bel)
        cls._cli_add_upload_bel(bel)

        return main