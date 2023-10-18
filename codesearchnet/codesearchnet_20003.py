def fields(self):
        """
        Return the fields specified in the pattern using Python's
        formatting mini-language.
        """
        parse = list(string.Formatter().parse(self.pattern))
        return [f for f in zip(*parse)[1] if f is not None]