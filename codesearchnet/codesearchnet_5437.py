def check_args(cls, config, options, args, parser, package_file=None):
        """
        Override in subclass if required.
        """
        if not args:
            parser.error("no input files specified")
        if not (package_file or options.package_file):
            parser.error("no package file specified")
        if not options.entry_point_process:
            parser.error("no entry point process specified")