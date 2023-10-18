def netspeed_by_addr(self, addr):
        """
        Returns NetSpeed name from address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        if self._databaseType == const.NETSPEED_EDITION:
            return const.NETSPEED_NAMES[self.id_by_addr(addr)]
        elif self._databaseType in (const.NETSPEED_EDITION_REV1,
                                    const.NETSPEED_EDITION_REV1_V6):
            ipnum = util.ip2long(addr)
            return self._get_org(ipnum)

        raise GeoIPError(
            'Invalid database type, expected NetSpeed or NetSpeedCell')