def _get_possible_day_starts(self, start_ut, end_ut, max_time_overnight=None):
        """
        Get all possible day start times between start_ut and end_ut
        Currently this function is used only by get_tripIs_within_range_by_dsut

        Parameters
        ----------
        start_ut : list<int>
            start time in unix time
        end_ut : list<int>
            end time in unix time
        max_time_overnight : list<int>
            the maximum length of time that a trip can take place on
            during the next day (i.e. after midnight run times like 25:35)

        Returns
        -------
        day_start_times_ut : list
            list of ints (unix times in seconds) for returning all possible day
            start times
        start_times_ds : list
            list of ints (unix times in seconds) stating the valid start time in
            day seconds
        end_times_ds : list
            list of ints (unix times in seconds) stating the valid end times in
            day_seconds
        """
        if max_time_overnight is None:
            # 7 hours:
            max_time_overnight = 7 * 60 * 60

        # sanity checks for the timezone parameter
        # assert timezone < 14
        # assert timezone > -14
        # tz_seconds = int(timezone*3600)
        assert start_ut < end_ut
        start_day_ut = self.day_start_ut(start_ut)
        # start_day_ds = int(start_ut+tz_seconds) % seconds_in_a_day  #??? needed?
        start_day_ds = start_ut - start_day_ut
        # assert (start_day_ut+tz_seconds) % seconds_in_a_day == 0
        end_day_ut = self.day_start_ut(end_ut)
        # end_day_ds = int(end_ut+tz_seconds) % seconds_in_a_day    #??? needed?
        # end_day_ds = end_ut - end_day_ut
        # assert (end_day_ut+tz_seconds) % seconds_in_a_day == 0

        # If we are early enough in a day that we might have trips from
        # the previous day still running, decrement the start day.
        if start_day_ds < max_time_overnight:
            start_day_ut = self.increment_day_start_ut(start_day_ut, n_days=-1)

        # day_start_times_ut = range(start_day_ut, end_day_ut+seconds_in_a_day, seconds_in_a_day)

        # Create a list of all possible day start times.  This is roughly
        # range(day_start_ut, day_end_ut+1day, 1day).
        day_start_times_ut = [start_day_ut]
        while day_start_times_ut[-1] < end_day_ut:
            day_start_times_ut.append(self.increment_day_start_ut(day_start_times_ut[-1]))

        start_times_ds = []
        end_times_ds = []
        # For every possible day start:
        for dsut in day_start_times_ut:
            # start day_seconds starts at either zero, or time - daystart
            day_start_ut = max(0, start_ut - dsut)
            start_times_ds.append(day_start_ut)
            # end day_seconds is time-day_start
            day_end_ut = end_ut - dsut
            end_times_ds.append(day_end_ut)
        # Return three tuples which can be zip:ped together.
        return day_start_times_ut, start_times_ds, end_times_ds