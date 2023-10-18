def id_by_addr(self, addr):
        """
        Returns the database ID for specified address.
        The ID might be useful as array index. 0 is unknown.

        :arg addr: IPv4 or IPv6 address (eg. 203.0.113.30)
        """
        if self._databaseType in (const.PROXY_EDITION, const.NETSPEED_EDITION_REV1, const.NETSPEED_EDITION_REV1_V6):
            raise GeoIPError('Invalid database type; this database is not supported')
        ipv = 6 if addr.find(':') >= 0 else 4
        if ipv == 4 and self._databaseType not in (const.COUNTRY_EDITION, const.NETSPEED_EDITION):
            raise GeoIPError('Invalid database type; this database supports IPv6 addresses, not IPv4')
        if ipv == 6 and self._databaseType != const.COUNTRY_EDITION_V6:
            raise GeoIPError('Invalid database type; this database supports IPv4 addresses, not IPv6')

        ipnum = util.ip2long(addr)
        return self._seek_country(ipnum) - const.COUNTRY_BEGIN