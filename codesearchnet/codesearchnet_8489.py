def contains_sequence(self, *items):
        """Asserts that val contains the given sequence of items in order."""
        if len(items) == 0:
            raise ValueError('one or more args must be given')
        else:
            try:
                for i in xrange(len(self.val) - len(items) + 1):
                    for j in xrange(len(items)):
                        if self.val[i+j] != items[j]:
                            break
                    else:
                        return self
            except TypeError:
                raise TypeError('val is not iterable')
        self._err('Expected <%s> to contain sequence %s, but did not.' % (self.val, self._fmt_items(items)))