def is_not_nan(self):
        """Asserts that val is real number and not NaN (not a number)."""
        self._validate_number()
        self._validate_real()
        if math.isnan(self.val):
            self._err('Expected not <NaN>, but was.')
        return self