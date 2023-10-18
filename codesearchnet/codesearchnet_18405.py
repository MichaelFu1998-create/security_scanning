def parse_argument(self, arg):
        """Parse a single argument.
        
        Lookup arg in self.specials, or call .to_python() if absent. Raise 
        BadArgument on errors.
        """
        lookup = self.casesensitive and arg or arg.lower()
        if lookup in self.special:
            return self.special[lookup]
        try:
            return self.to_python(arg, *self.args, **self.kw)
        except Exception, e:
            raise BadArgument(arg, str(e))