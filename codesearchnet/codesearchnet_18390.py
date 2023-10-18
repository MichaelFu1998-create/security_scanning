def _parse_positional_arguments(self, argv):
        """Parse the positional arguments part of an argument list.
        argv <list str>:
            List of arguments. Will be altered.
        """
        for posarg in self.positional_args:
            posarg.parse(argv)
        if argv:
            if None in [p.nargs for p in self.positional_args]:
                msg = '%s too many argument%s given'
                plural_s = len(argv) > 1 and 's' or ''
                raise BadNumberOfArguments(message=msg % (len(argv), plural_s))
            msg = 'This program accepts exactly %s positional arguments (%s given).'
            required = len([p.nargs for p in self.positional_args])
            raise BadNumberOfArguments(message=msg % (required, required + len(argv)))