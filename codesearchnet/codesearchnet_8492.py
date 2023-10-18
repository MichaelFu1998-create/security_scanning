def is_empty(self):
        """Asserts that val is empty."""
        if len(self.val) != 0:
            if isinstance(self.val, str_types):
                self._err('Expected <%s> to be empty string, but was not.' % self.val)
            else:
                self._err('Expected <%s> to be empty, but was not.' % self.val)
        return self