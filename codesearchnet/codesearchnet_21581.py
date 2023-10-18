def tz(self):
        """Return the timezone. If none is set use system timezone"""
        if not self._tz:
            self._tz = tzlocal.get_localzone().zone
        return self._tz