def get_hex(self):
        """Return the hexadecimal notation of the address/netmask."""
        return _convert(self._ip_dec, notation=IP_HEX,
                        inotation=IP_DEC, _check=False, _isnm=self._isnm)