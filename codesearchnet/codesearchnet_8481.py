def is_same_as(self, other):
        """Asserts that the val is identical to other, via 'is' compare."""
        if self.val is not other:
            self._err('Expected <%s> to be identical to <%s>, but was not.' % (self.val, other))
        return self