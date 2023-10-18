def get_tripIs_within_range_by_dsut(self,
                                        start_time_ut,
                                        end_time_ut):
        """
        Obtain a list of trip_Is that take place during a time interval.
        The trip needs to be only partially overlapping with the given time interval.
        The grouping by dsut (day_start_ut) is required as same trip_I could
        take place on multiple days.

        Parameters
        ----------
        start_time_ut : int
            start of the time interval in unix time (seconds)
        end_time_ut: int
            end of the time interval in unix time (seconds)

        Returns
        -------
        trip_I_dict: dict
            keys: day_start_times to list of integers (trip_Is)
        """
        cur = self.conn.cursor()
        assert start_time_ut <= end_time_ut
        dst_ut, st_ds, et_ds = \
            self._get_possible_day_starts(start_time_ut, end_time_ut, 7)
        # noinspection PyTypeChecker
        assert len(dst_ut) >= 0
        trip_I_dict = {}
        for day_start_ut, start_ds, end_ds in \
                zip(dst_ut, st_ds, et_ds):
            query = """
                        SELECT distinct(trip_I)
                        FROM days
                            JOIN trips
                            USING(trip_I)
                        WHERE
                            (days.day_start_ut == ?)
                            AND (
                                    (trips.start_time_ds <= ?)
                                    AND
                                    (trips.end_time_ds >= ?)
                                )
                        """
            params = (day_start_ut, end_ds, start_ds)
            trip_Is = [el[0] for el in cur.execute(query, params)]
            if len(trip_Is) > 0:
                trip_I_dict[day_start_ut] = trip_Is
        return trip_I_dict