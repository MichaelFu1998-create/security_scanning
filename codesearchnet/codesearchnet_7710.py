def _setup_segments(self):
        """
        Parses the database file to determine what kind of database is
        being used and setup segment sizes and start points that will
        be used by the seek*() methods later.
        """
        self._databaseType = const.COUNTRY_EDITION
        self._recordLength = const.STANDARD_RECORD_LENGTH
        self._databaseSegments = const.COUNTRY_BEGIN

        filepos = self._fp.tell()
        self._fp.seek(-3, os.SEEK_END)

        for i in range(const.STRUCTURE_INFO_MAX_SIZE):
            chars = chr(255) * 3
            delim = self._fp.read(3)

            if PY3 and type(delim) is bytes:
                delim = delim.decode(ENCODING)

            if PY2:
                chars = chars.decode(ENCODING)
                if type(delim) is str:
                    delim = delim.decode(ENCODING)

            if delim == chars:
                byte = self._fp.read(1)
                self._databaseType = ord(byte)

                # Compatibility with databases from April 2003 and earlier
                if self._databaseType >= 106:
                    self._databaseType -= 105

                if self._databaseType == const.REGION_EDITION_REV0:
                    self._databaseSegments = const.STATE_BEGIN_REV0

                elif self._databaseType == const.REGION_EDITION_REV1:
                    self._databaseSegments = const.STATE_BEGIN_REV1

                elif self._databaseType in (const.CITY_EDITION_REV0,
                                            const.CITY_EDITION_REV1,
                                            const.CITY_EDITION_REV1_V6,
                                            const.ORG_EDITION,
                                            const.ISP_EDITION,
                                            const.NETSPEED_EDITION_REV1,
                                            const.NETSPEED_EDITION_REV1_V6,
                                            const.ASNUM_EDITION,
                                            const.ASNUM_EDITION_V6):
                    self._databaseSegments = 0
                    buf = self._fp.read(const.SEGMENT_RECORD_LENGTH)

                    if PY3 and type(buf) is bytes:
                        buf = buf.decode(ENCODING)

                    for j in range(const.SEGMENT_RECORD_LENGTH):
                        self._databaseSegments += (ord(buf[j]) << (j * 8))

                    LONG_RECORDS = (const.ORG_EDITION, const.ISP_EDITION)
                    if self._databaseType in LONG_RECORDS:
                        self._recordLength = const.ORG_RECORD_LENGTH
                break
            else:
                self._fp.seek(-4, os.SEEK_CUR)

        self._fp.seek(filepos, os.SEEK_SET)