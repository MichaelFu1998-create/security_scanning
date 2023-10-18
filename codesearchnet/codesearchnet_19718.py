def get_bin(self):
        """Return the binary notation of the address/netmask."""
        return _convert(self._ip_dec, notation=IP_BIN,
                        inotation=IP_DEC, _check=False, _isnm=self._isnm)