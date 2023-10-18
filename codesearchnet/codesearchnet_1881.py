def format(self, o, context, maxlevels, level):
        """Format o for a specific context, returning a string
        and flags indicating whether the representation is 'readable'
        and whether the o represents a recursive construct.
        """
        return _safe_repr(o, context, maxlevels, level)