def isoformat(self):
        """Return the date formatted according to ISO.

        This is 'YYYY-MM-DD'.

        References:
        - http://www.w3.org/TR/NOTE-datetime
        - http://www.cl.cam.ac.uk/~mgk25/iso-time.html
        """
        # return "%04d-%02d-%02d" % (self._year, self._month, self._day)
        return "%s-%s-%s" % (str(self._year).zfill(4), str(self._month).zfill(2), str(self._day).zfill(2))