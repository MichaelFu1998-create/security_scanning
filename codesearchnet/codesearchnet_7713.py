def _get_region(self, ipnum):
        """
        Seek and return the region information.
        Returns dict containing country_code and region_code.

        :arg ipnum: Result of ip2long conversion
        """
        region_code = None
        country_code = None
        seek_country = self._seek_country(ipnum)

        def get_region_code(offset):
            region1 = chr(offset // 26 + 65)
            region2 = chr(offset % 26 + 65)
            return ''.join([region1, region2])

        if self._databaseType == const.REGION_EDITION_REV0:
            seek_region = seek_country - const.STATE_BEGIN_REV0
            if seek_region >= 1000:
                country_code = 'US'
                region_code = get_region_code(seek_region - 1000)
            else:
                country_code = const.COUNTRY_CODES[seek_region]
        elif self._databaseType == const.REGION_EDITION_REV1:
            seek_region = seek_country - const.STATE_BEGIN_REV1
            if seek_region < const.US_OFFSET:
                pass
            elif seek_region < const.CANADA_OFFSET:
                country_code = 'US'
                region_code = get_region_code(seek_region - const.US_OFFSET)
            elif seek_region < const.WORLD_OFFSET:
                country_code = 'CA'
                region_code = get_region_code(seek_region - const.CANADA_OFFSET)
            else:
                index = (seek_region - const.WORLD_OFFSET) // const.FIPS_RANGE
                if index < len(const.COUNTRY_CODES):
                    country_code = const.COUNTRY_CODES[index]
        elif self._databaseType in const.CITY_EDITIONS:
            rec = self._get_record(ipnum)
            region_code = rec.get('region_code')
            country_code = rec.get('country_code')

        return {'country_code': country_code, 'region_code': region_code}