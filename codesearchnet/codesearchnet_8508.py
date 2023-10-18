def is_digit(self):
        """Asserts that val is non-empty string and all characters are digits."""
        if not isinstance(self.val, str_types):
            raise TypeError('val is not a string')
        if len(self.val) == 0:
            raise ValueError('val is empty')
        if not self.val.isdigit():
            self._err('Expected <%s> to contain only digits, but did not.' % self.val)
        return self