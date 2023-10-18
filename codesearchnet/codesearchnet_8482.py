def is_not_same_as(self, other):
        """Asserts that the val is not identical to other, via 'is' compare."""
        if self.val is other:
            self._err('Expected <%s> to be not identical to <%s>, but was.' % (self.val, other))
        return self