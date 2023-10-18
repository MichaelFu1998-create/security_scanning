def increment_day_start_ut(self, day_start_ut, n_days=1):
        """Increment the GTFS-definition of "day start".

        Parameters
        ----------
        day_start_ut : int
            unixtime of the previous start of day.  If this time is between
            12:00 or greater, there *will* be bugs.  To solve this, run the
            input through day_start_ut first.
        n_days: int
            number of days to increment
        """
        old_tz = self.set_current_process_time_zone()
        day0 = time.localtime(day_start_ut + 43200)  # time of noon
        dayN = time.mktime(day0[:2] +  # YYYY, MM
                           (day0[2] + n_days,) +  # DD
                           (12, 00, 0, 0, 0, -1)) - 43200  # HHMM, etc.  Minus 12 hours.
        set_process_timezone(old_tz)
        return dayN