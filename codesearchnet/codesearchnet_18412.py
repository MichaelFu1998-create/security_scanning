def parse(self, argv):
        """Pop, parse and return the first arg from argv.
        
        The arg will be repeatedly .split(x, 1) based on self.get_separator() and the 
        (optionally stripped) items will be parsed by self.format and returned
        as a list. 

        Raise BadNumberOfArguments or BadArgument on errors.
         
        NOTE: args will be modified.
        """
        if not argv:
            raise BadNumberOfArguments(1, 0)
        remainder = argv.pop(0)
        lookup = self.casesensitive and remainder or remainder.lower()
        if lookup in self.special:
            return self.special[lookup]
        values = []
        for i, format in enumerate(self.format[:-1]):
            print i, self.get_separator(i)
            try:
                arg, remainder = remainder.split(self.get_separator(i + 1), 1)
            except:
                raise BadArgument(remainder, 'does not contain required separator ' + repr(self.get_separator(i + 1)))
            if self.strip:
                arg = arg.strip()
            values.append(format.parse([arg]))
        if self.strip:
            remainder = remainder.strip()
        values.append(format.parse([remainder]))
        return values