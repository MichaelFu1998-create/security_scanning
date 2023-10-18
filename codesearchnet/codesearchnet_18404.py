def parsestr(self, argstr):
        """Parse arguments found in settings files.
        
        argstr is the string that should be parsed. Use e.g. '""' to pass an
        empty string.

        if self.nargs > 1 a list of parsed values will be returned.

        NOTE: formats with nargs == 0 or None probably want to override this 
        method.
        """
        argv = shlex.split(argstr, comments=True)
        if len(argv) != self.nargs:
            raise BadNumberOfArguments(self.nargs, len(argv))
        return self.parse(argv)