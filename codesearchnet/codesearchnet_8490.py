def contains_duplicates(self):
        """Asserts that val is iterable and contains duplicate items."""
        try:
            if len(self.val) != len(set(self.val)):
                return self
        except TypeError:
            raise TypeError('val is not iterable')
        self._err('Expected <%s> to contain duplicates, but did not.' % self.val)