def get_cli(cls) -> click.Group:
        """Build a :mod:`click` CLI main function.

        :param Type[AbstractManager] cls: A Manager class
        :return: The main function for click
        """
        group_help = 'Default connection at {}\n\nusing Bio2BEL v{}'.format(cls._get_connection(), get_version())

        @click.group(help=group_help)
        @click.option('-c', '--connection', default=cls._get_connection(),
                      help='Defaults to {}'.format(cls._get_connection()))
        @click.pass_context
        def main(ctx, connection):
            """Bio2BEL CLI."""
            logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            logging.getLogger('bio2bel.utils').setLevel(logging.WARNING)
            ctx.obj = cls(connection=connection)

        return main