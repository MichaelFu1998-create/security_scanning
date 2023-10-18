def is_not_equal_to(self, other):
        """Asserts that val is not equal to other."""
        if self.val == other:
            self._err('Expected <%s> to be not equal to <%s>, but was.' % (self.val, other))
        return self