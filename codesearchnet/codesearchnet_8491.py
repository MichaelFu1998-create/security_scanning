def does_not_contain_duplicates(self):
        """Asserts that val is iterable and does not contain any duplicate items."""
        try:
            if len(self.val) == len(set(self.val)):
                return self
        except TypeError:
            raise TypeError('val is not iterable')
        self._err('Expected <%s> to not contain duplicates, but did.' % self.val)