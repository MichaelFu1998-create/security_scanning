def _seek_country(self, ipnum):
        """
        Using the record length and appropriate start points, seek to the
        country that corresponds to the converted IP address integer.
        Return offset of record.

        :arg ipnum: Result of ip2long conversion
        """
        try:
            offset = 0
            seek_depth = 127 if len(str(ipnum)) > 10 else 31

            for depth in range(seek_depth, -1, -1):
                if self._flags & const.MEMORY_CACHE:
                    startIndex = 2 * self._recordLength * offset
                    endIndex = startIndex + (2 * self._recordLength)
                    buf = self._memory[startIndex:endIndex]
                else:
                    startIndex = 2 * self._recordLength * offset
                    readLength = 2 * self._recordLength
                    try:
                        self._lock.acquire()
                        self._fp.seek(startIndex, os.SEEK_SET)
                        buf = self._fp.read(readLength)
                    finally:
                        self._lock.release()

                if PY3 and type(buf) is bytes:
                    buf = buf.decode(ENCODING)

                x = [0, 0]
                for i in range(2):
                    for j in range(self._recordLength):
                        byte = buf[self._recordLength * i + j]
                        x[i] += ord(byte) << (j * 8)
                if ipnum & (1 << depth):
                    if x[1] >= self._databaseSegments:
                        self._netmask = seek_depth - depth + 1
                        return x[1]
                    offset = x[1]
                else:
                    if x[0] >= self._databaseSegments:
                        self._netmask = seek_depth - depth + 1
                        return x[0]
                    offset = x[0]
        except (IndexError, UnicodeDecodeError):
            pass

        raise GeoIPError('Corrupt database')