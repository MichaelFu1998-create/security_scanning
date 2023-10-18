def raw(self, clean=False):
        """Raw block name
        args:
            clean (bool): clean name
        returns:
            str
        """
        try:
            return self.tokens[0].raw(clean)
        except (AttributeError, TypeError):
            pass