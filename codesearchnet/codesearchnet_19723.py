def get_bits(self):
        """Return the bits notation of the netmask."""
        return _convert(self._ip, notation=NM_BITS,
                        inotation=IP_DOT, _check=False, _isnm=self._isnm)