def set(self, ip, notation=IP_UNKNOWN):
        """Set the IP address/netmask."""
        self._ip_dec = int(_convert(ip, notation=IP_DEC, inotation=notation,
                                    _check=True, _isnm=self._isnm))
        self._ip = _convert(self._ip_dec, notation=IP_DOT, inotation=IP_DEC,
                            _check=False, _isnm=self._isnm)