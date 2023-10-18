def _add(self, other):
        """Sum two IP addresses."""
        if isinstance(other, self.__class__):
            sum_ = self._ip_dec + other._ip_dec
        elif isinstance(other, int):
            sum_ = self._ip_dec + other
        else:
            other = self.__class__(other)
            sum_ = self._ip_dec + other._ip_dec
        return sum_