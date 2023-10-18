def is_in(self, *items):
        """Asserts that val is equal to one of the given items."""
        if len(items) == 0:
            raise ValueError('one or more args must be given')
        else:
            for i in items:
                if self.val == i:
                    return self
        self._err('Expected <%s> to be in %s, but was not.' % (self.val, self._fmt_items(items)))