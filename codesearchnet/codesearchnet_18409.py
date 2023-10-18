def parse(self, argv):
        """Pop, parse and return the first arg from argv.
        
        The arg will be .split() based on self.separator and the (optionally 
        stripped) items will be parsed by self.format and returned as a list. 

        Raise BadNumberOfArguments or BadArgument on errors.
         
        NOTE: args will be modified.
        """
        if not argv:
            raise BadNumberOfArguments(1, 0)
        argument = argv.pop(0)
        lookup = self.casesensitive and argument or argument.lower()
        if lookup in self.special:
            return self.special[lookup]
        argv = [(self.strip and s.strip() or s) for s in argument.split(self.separator)]
        values = []
        while argv:
            values.append(self.format.parse(argv))
        return values