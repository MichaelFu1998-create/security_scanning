def is_lower(self):
        """Asserts that val is non-empty string and all characters are lowercase."""
        if not isinstance(self.val, str_types):
            raise TypeError('val is not a string')
        if len(self.val) == 0:
            raise ValueError('val is empty')
        if self.val != self.val.lower():
            self._err('Expected <%s> to contain only lowercase chars, but did not.' % self.val)
        return self