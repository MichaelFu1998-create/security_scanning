def parse(self, argv):
        """Pop, parse and return the first self.nargs items from args.

        if self.nargs > 1 a list of parsed values will be returned.
        
        Raise BadNumberOfArguments or BadArgument on errors.
         
        NOTE: argv may be modified in place by this method.
        """
        if len(argv) < self.nargs:
            raise BadNumberOfArguments(self.nargs, len(argv))
        if self.nargs == 1:
            return self.parse_argument(argv.pop(0))
        return [self.parse_argument(argv.pop(0)) for tmp in range(self.nargs)]