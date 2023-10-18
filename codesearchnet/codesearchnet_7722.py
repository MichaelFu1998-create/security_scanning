def country_name_by_addr(self, addr):
        """
        Returns full country name for specified IP address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        VALID_EDITIONS = (const.COUNTRY_EDITION, const.COUNTRY_EDITION_V6)
        if self._databaseType in VALID_EDITIONS:
            country_id = self.id_by_addr(addr)
            return const.COUNTRY_NAMES[country_id]
        elif self._databaseType in const.CITY_EDITIONS:
            return self.record_by_addr(addr).get('country_name')
        else:
            message = 'Invalid database type, expected Country or City'
            raise GeoIPError(message)