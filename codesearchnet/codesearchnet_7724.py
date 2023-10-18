def org_by_addr(self, addr):
        """
        Returns Organization, ISP, or ASNum name for given IP address.

        :arg addr: IP address (e.g. 203.0.113.30)
        """
        valid = (const.ORG_EDITION, const.ISP_EDITION,
                 const.ASNUM_EDITION, const.ASNUM_EDITION_V6)
        if self._databaseType not in valid:
            message = 'Invalid database type, expected Org, ISP or ASNum'
            raise GeoIPError(message)

        ipnum = util.ip2long(addr)
        return self._get_org(ipnum)