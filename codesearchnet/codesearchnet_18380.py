def parse(self, argv):
        """Consume and process arguments and store the result.
        
        argv is the list of arguments to parse (will be modified).
        
        Recurring PositionalArgumants get a list as .value.
        
        Optional PositionalArguments that do not get any arguments to parse get
        None as .value, or [] if recurring. 
        """
        if not argv and self.optional:
            self.value = [] if self.recurring else None
            return
        try:
            value = self.format.parse(argv)
            if not self.recurring:
                self.value = value
                return
            self.value = [value]
            while argv:
                self.value.append(self.format.parse(argv))
        except formats.BadNumberOfArguments, e:
            raise BadNumberOfArguments(self.displayname, e.required, e.given)
        except formats.BadArgument, e:
            raise BadArgument(self.displayname, e.argument, e.details)