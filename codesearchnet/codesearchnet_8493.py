def is_not_empty(self):
        """Asserts that val is not empty."""
        if len(self.val) == 0:
            if isinstance(self.val, str_types):
                self._err('Expected not empty string, but was empty.')
            else:
                self._err('Expected not empty, but was empty.')
        return self