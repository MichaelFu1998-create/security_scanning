def _get_record(self, ipnum):
        """
        Populate location dict for converted IP.
        Returns dict with numerous location properties.

        :arg ipnum: Result of ip2long conversion
        """
        seek_country = self._seek_country(ipnum)
        if seek_country == self._databaseSegments:
            return {}

        read_length = (2 * self._recordLength - 1) * self._databaseSegments
        try:
            self._lock.acquire()
            self._fp.seek(seek_country + read_length, os.SEEK_SET)
            buf = self._fp.read(const.FULL_RECORD_LENGTH)
        finally:
            self._lock.release()

        if PY3 and type(buf) is bytes:
            buf = buf.decode(ENCODING)

        record = {
            'dma_code': 0,
            'area_code': 0,
            'metro_code': None,
            'postal_code': None
        }

        latitude = 0
        longitude = 0

        char = ord(buf[0])
        record['country_code'] = const.COUNTRY_CODES[char]
        record['country_code3'] = const.COUNTRY_CODES3[char]
        record['country_name'] = const.COUNTRY_NAMES[char]
        record['continent'] = const.CONTINENT_NAMES[char]

        def read_data(buf, pos):
            cur = pos
            while buf[cur] != '\0':
                cur += 1
            return cur, buf[pos:cur] if cur > pos else None

        offset, record['region_code'] = read_data(buf, 1)
        offset, record['city'] = read_data(buf, offset + 1)
        offset, record['postal_code'] = read_data(buf, offset + 1)
        offset = offset + 1

        for j in range(3):
            latitude += (ord(buf[offset + j]) << (j * 8))

        for j in range(3):
            longitude += (ord(buf[offset + j + 3]) << (j * 8))

        record['latitude'] = (latitude / 10000.0) - 180.0
        record['longitude'] = (longitude / 10000.0) - 180.0

        if self._databaseType in (const.CITY_EDITION_REV1, const.CITY_EDITION_REV1_V6):
            if record['country_code'] == 'US':
                dma_area = 0
                for j in range(3):
                    dma_area += ord(buf[offset + j + 6]) << (j * 8)

                record['dma_code'] = int(floor(dma_area / 1000))
                record['area_code'] = dma_area % 1000
                record['metro_code'] = const.DMA_MAP.get(record['dma_code'])

        params = (record['country_code'], record['region_code'])
        record['time_zone'] = time_zone_by_country_and_region(*params)

        return record