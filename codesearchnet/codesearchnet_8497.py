def is_inf(self):
        """Asserts that val is real number and Inf (infinity)."""
        self._validate_number()
        self._validate_real()
        if not math.isinf(self.val):
            self._err('Expected <%s> to be <Inf>, but was not.' % self.val)
        return self