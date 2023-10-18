def _get_org(self, ipnum):
        """
        Seek and return organization or ISP name for ipnum.
        Return org/isp name.

        :arg ipnum: Result of ip2long conversion
        """
        seek_org = self._seek_country(ipnum)
        if seek_org == self._databaseSegments:
            return None

        read_length = (2 * self._recordLength - 1) * self._databaseSegments
        try:
            self._lock.acquire()
            self._fp.seek(seek_org + read_length, os.SEEK_SET)
            buf = self._fp.read(const.MAX_ORG_RECORD_LENGTH)
        finally:
            self._lock.release()

        if PY3 and type(buf) is bytes:
            buf = buf.decode(ENCODING)

        return buf[:buf.index(chr(0))]