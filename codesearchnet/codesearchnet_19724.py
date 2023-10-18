def get_wildcard(self):
        """Return the wildcard bits notation of the netmask."""
        return _convert(self._ip, notation=NM_WILDCARD,
                        inotation=IP_DOT, _check=False, _isnm=self._isnm)