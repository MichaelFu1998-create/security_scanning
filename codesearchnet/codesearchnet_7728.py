def region_by_addr(self, addr):
        """
        Returns dictionary containing `country_code` and `region_code`.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType not in const.REGION_CITY_EDITIONS:
            message = 'Invalid database type, expected Region or City'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        return self._get_region(ipnum)