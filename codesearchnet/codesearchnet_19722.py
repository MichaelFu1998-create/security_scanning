def _sub(self, other):
        """Subtract two IP addresses."""
        if isinstance(other, self.__class__):
            sub = self._ip_dec - other._ip_dec
        if isinstance(other, int):
            sub = self._ip_dec - other
        else:
            other = self.__class__(other)
            sub = self._ip_dec - other._ip_dec
        return sub