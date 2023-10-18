def update(self, new_val):
        """Update the estimate.

        Parameters
        ----------
        new_val: float
            new observated value of estimated quantity.
        """
        if self._value is None:
            self._value = new_val
        else:
            self._value = self._gamma * self._value + (1.0 - self._gamma) * new_val