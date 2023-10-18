def _default(self):
        """
        Return the default argument, formatted nicely.

        """
        try:
            # Check if it's iterable
            iter(self.default)
        except TypeError:
            return repr(self.default)

        # This is to look for unparsable values, and if we find one, we try to
        # directly parse the string
        for v in self.default:
            if isinstance(v, Unparseable):
                default = self._default_value_only()
                if default:
                    return default
        # Otherwise just make it a string and go
        return ', '.join(str(v) for v in self.default)