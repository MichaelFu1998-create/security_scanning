def utctimetuple(self):
        "Return UTC time tuple compatible with time.gmtime()."
        y, m, d = self.year, self.month, self.day
        hh, mm, ss = self.hour, self.minute, self.second
        offset = self._utcoffset()
        if offset:  # neither None nor 0
            mm -= offset
            y, m, d, hh, mm, ss, _ = _normalize_datetime(
                y, m, d, hh, mm, ss, 0, ignore_overflow=True)
        return _build_struct_time(y, m, d, hh, mm, ss, 0)