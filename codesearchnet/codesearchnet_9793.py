def day_start_ut(self, ut):
        """
        Convert unixtime to unixtime on GTFS start-of-day.

        GTFS defines the start of a day as "noon minus 12 hours" to solve
        most DST-related problems. This means that on DST-changing days,
        the day start isn't midnight. This function isn't idempotent.
        Running it twice on the "move clocks backwards" day will result in
        being one day too early.

        Parameters
        ----------
        ut: int
            Unixtime

        Returns
        -------
        ut: int
            Unixtime corresponding to start of day
        """
        # set timezone to the one of gtfs
        old_tz = self.set_current_process_time_zone()
        ut = time.mktime(time.localtime(ut)[:3] + (12, 00, 0, 0, 0, -1)) - 43200
        set_process_timezone(old_tz)
        return ut