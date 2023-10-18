def create_parser(self, prog_name, subcommand):
        """
        Create argument parser and deal with ``add_arguments``.
        This method should not be overriden.

        :param prog_name: Name of the command (argv[0])
        :return: ArgumentParser
        """
        parser = argparse.ArgumentParser(prog_name, subcommand)
        # Add generic arguments here
        self.add_arguments(parser)
        return parser