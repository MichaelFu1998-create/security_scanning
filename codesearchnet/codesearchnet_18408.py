def parsestr(self, argstr):
        """Parse arguments found in settings files.
        
        Use the values in self.true for True in settings files, or those in 
        self.false for False, case insensitive.
        """
        argv = shlex.split(argstr, comments=True)
        if len(argv) != 1:
            raise BadNumberOfArguments(1, len(argv))
        arg = argv[0]
        lower = arg.lower()
        if lower in self.true:
            return True
        if lower in self.false:
            return False
        raise BadArgument(arg, "Allowed values are " + self.allowed + '.')