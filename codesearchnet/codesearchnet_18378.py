def parse(self, argv, usedname, location):
        """Consume and process arguments and store the result.
        ARGS:
        argv <list str>:
            The argument list to parse.
        usedname <str>:
            The string used by the user to invoke the option.
        location <str>:
            A user friendly sring describing where the parser got this
            data from.

        """
        try:
            value = self.format.parse(argv)
        except formats.BadNumberOfArguments, e:
            raise BadNumberOfArguments(usedname, e.required, e.supplied)
        except formats.BadArgument, e:
            raise BadArgument(usedname, e.argument, e.message)
        if self.recurring:
            self.value.append(value)
        else:
            self.value = value
        self.location = location