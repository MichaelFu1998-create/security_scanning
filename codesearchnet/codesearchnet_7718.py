def country_code_by_addr(self, addr):
        """
        Returns 2-letter country code (e.g. US) from IP address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        VALID_EDITIONS = (const.COUNTRY_EDITION, const.COUNTRY_EDITION_V6)
        if self._databaseType in VALID_EDITIONS:
            country_id = self.id_by_addr(addr)
            return const.COUNTRY_CODES[country_id]
        elif self._databaseType in const.REGION_CITY_EDITIONS:
            return self.region_by_addr(addr).get('country_code')

        raise GeoIPError('Invalid database type, expected Country, City or Region')