def is_equal_to_ignoring_case(self, other):
        """Asserts that val is case-insensitive equal to other."""
        if not isinstance(self.val, str_types):
            raise TypeError('val is not a string')
        if not isinstance(other, str_types):
            raise TypeError('given arg must be a string')
        if self.val.lower() != other.lower():
            self._err('Expected <%s> to be case-insensitive equal to <%s>, but was not.' % (self.val, other))
        return self