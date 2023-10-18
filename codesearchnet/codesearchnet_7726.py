def record_by_addr(self, addr):
        """
        Returns dictionary with city data containing `country_code`, `country_name`,
        `region`, `city`, `postal_code`, `latitude`, `longitude`, `dma_code`,
        `metro_code`, `area_code`, `region_code` and `time_zone`.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType not in const.CITY_EDITIONS:
            message = 'Invalid database type, expected City'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        rec = self._get_record(ipnum)
        if not rec:
            return None

        return rec