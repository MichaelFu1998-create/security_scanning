def is_length(self, length):
        """Asserts that val is the given length."""
        if type(length) is not int:
            raise TypeError('given arg must be an int')
        if length < 0:
            raise ValueError('given arg must be a positive int')
        if len(self.val) != length:
            self._err('Expected <%s> to be of length <%d>, but was <%d>.' % (self.val, length, len(self.val)))
        return self