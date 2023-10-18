def is_alpha(self):
        """Asserts that val is non-empty string and all characters are alphabetic."""
        if not isinstance(self.val, str_types):
            raise TypeError('val is not a string')
        if len(self.val) == 0:
            raise ValueError('val is empty')
        if not self.val.isalpha():
            self._err('Expected <%s> to contain only alphabetic chars, but did not.' % self.val)
        return self