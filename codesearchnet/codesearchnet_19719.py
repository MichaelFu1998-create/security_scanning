def get_oct(self):
        """Return the octal notation of the address/netmask."""
        return _convert(self._ip_dec, notation=IP_OCT,
                        inotation=IP_DEC, _check=False, _isnm=self._isnm)