def time_zone_by_addr(self, addr):
        """
        Returns time zone in tzdata format (e.g. America/New_York or Europe/Paris)

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType not in const.CITY_EDITIONS:
            message = 'Invalid database type, expected City'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        return self._get_record(ipnum).get('time_zone')