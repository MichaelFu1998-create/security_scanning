def run_from_argv(self, argv):
        """
        Called by the system when executing the command from the command line.
        This should not be overridden.

        :param argv: Arguments from command line
        """
        parser = self.create_parser(argv[0], argv[1])
        options = parser.parse_args(argv[2:])
        cmd_options = vars(options)
        args = cmd_options.pop('args', ())
        self.handle(*args, **cmd_options)