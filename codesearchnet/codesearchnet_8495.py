def is_nan(self):
        """Asserts that val is real number and NaN (not a number)."""
        self._validate_number()
        self._validate_real()
        if not math.isnan(self.val):
            self._err('Expected <%s> to be <NaN>, but was not.' % self.val)
        return self