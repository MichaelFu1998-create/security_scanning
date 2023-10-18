def insert(self, name, index, value):
        """Insert a value at the passed index in the named header."""
        return self.headers.insert(index, value)