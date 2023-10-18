def insert(self, name, index, value):
        """Insert a value at the passed index in the named header."""
        return self._sequence[name].insert(index, value)