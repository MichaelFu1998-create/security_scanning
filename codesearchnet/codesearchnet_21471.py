def items(self):
        """
        A generator yielding ``(key, value)`` attribute pairs, sorted by key name.
        """
        for key in sorted(self.attrs):
            yield key, self.attrs[key]