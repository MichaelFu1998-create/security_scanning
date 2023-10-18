def is_not_inf(self):
        """Asserts that val is real number and not Inf (infinity)."""
        self._validate_number()
        self._validate_real()
        if math.isinf(self.val):
            self._err('Expected not <Inf>, but was.')
        return self