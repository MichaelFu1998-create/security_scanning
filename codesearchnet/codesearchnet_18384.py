def getparam(self, key):
        """Get option or positional argument, by name, index or abbreviation.
        
        Abbreviations must be prefixed by a '-' character, like so: ui['-a']
        """
        try:
            return self.options[key]
        except:
            pass
        for posarg in self.positional_args:
            if posarg.name == key:
                return posarg
        try:
            return self.abbreviations[key[1:]]
        except:
            raise KeyError('no such option or positional argument')