def unlocalized_datetime_to_ut_seconds(self, unlocalized_datetime):
        """
        Convert datetime (in GTFS timezone) to unixtime

        Parameters
        ----------
        unlocalized_datetime : datetime.datetime
            (tz coerced to GTFS timezone, should NOT be UTC.)

        Returns
        -------
        output : int (unixtime)
        """
        loc_dt = self._timezone.localize(unlocalized_datetime)
        unixtime_seconds = calendar.timegm(loc_dt.utctimetuple())
        return unixtime_seconds