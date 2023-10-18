def utcoffset(self):
        """Return the timezone offset in minutes east of UTC (negative west of
        UTC)."""
        if self._tzinfo is None:
            return None
        offset = self._tzinfo.utcoffset(self)
        offset = _check_utc_offset("utcoffset", offset)
        if offset is not None:
            offset = timedelta._create(0, offset * 60, 0, True)
        return offset