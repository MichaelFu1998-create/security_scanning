def _cmp_prepare(self, other):
        """Prepare the item to be compared with this address/netmask."""
        if isinstance(other, self.__class__):
            return other._ip_dec
        elif isinstance(other, int):
            # NOTE: this hides the fact that "other" can be a non valid IP/nm.
            return other
        return self.__class__(other)._ip_dec