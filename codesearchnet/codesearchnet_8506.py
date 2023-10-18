def matches(self, pattern):
        """Asserts that val is string and matches regex pattern."""
        if not isinstance(self.val, str_types):
            raise TypeError('val is not a string')
        if not isinstance(pattern, str_types):
            raise TypeError('given pattern arg must be a string')
        if len(pattern) == 0:
            raise ValueError('given pattern arg must not be empty')
        if re.search(pattern, self.val) is None:
            self._err('Expected <%s> to match pattern <%s>, but did not.' % (self.val, pattern))
        return self