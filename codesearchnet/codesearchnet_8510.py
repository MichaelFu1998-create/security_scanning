def is_upper(self):
        """Asserts that val is non-empty string and all characters are uppercase."""
        if not isinstance(self.val, str_types):
            raise TypeError('val is not a string')
        if len(self.val) == 0:
            raise ValueError('val is empty')
        if self.val != self.val.upper():
            self._err('Expected <%s> to contain only uppercase chars, but did not.' % self.val)
        return self