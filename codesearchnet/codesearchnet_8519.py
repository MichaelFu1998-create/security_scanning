def exists(self):
        """Asserts that val is a path and that it exists."""
        if not isinstance(self.val, str_types):
            raise TypeError('val is not a path')
        if not os.path.exists(self.val):
            self._err('Expected <%s> to exist, but was not found.' % self.val)
        return self