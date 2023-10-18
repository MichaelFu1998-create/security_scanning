def parse_argv(self, argv=None, location='Command line.'):
        """Parse command line arguments.
        
        args <list str> or None:
            The argument list to parse. None means use a copy of sys.argv. argv[0] is
            ignored.
        location = '' <str>:
            A user friendly string describing where the parser got this
            data from. '' means use "Command line." if args == None, and
            "Builtin default." otherwise.
            
        """
        if argv is None:
            argv = list(sys.argv)
        argv.pop(0)
        self._parse_options(argv, location)
        self._parse_positional_arguments(argv)