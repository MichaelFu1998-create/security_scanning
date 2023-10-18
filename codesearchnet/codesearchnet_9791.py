def get_events_by_tripI_and_dsut(self, trip_I, day_start_ut,
                                     start_ut=None, end_ut=None):
        """
        Get trip data as a list of events (i.e. dicts).

        Parameters
        ----------
        trip_I : int
            shorthand index of the trip.
        day_start_ut : int
            the start time of the day in unix time (seconds)
        start_ut : int, optional
            consider only events that start after this time
            If not specified, this filtering is not applied.
        end_ut : int, optional
            Consider only events that end before this time
            If not specified, this filtering is not applied.

        Returns
        -------
        events: list of dicts
            each element contains the following data:
                from_stop: int (stop_I)
                to_stop: int (stop_I)
                dep_time_ut: int (in unix time)
                arr_time_ut: int (in unix time)
        """
        # for checking input:
        assert day_start_ut <= start_ut
        assert day_start_ut <= end_ut
        assert start_ut <= end_ut
        events = []
        # check that trip takes place on that day:
        if not self.tripI_takes_place_on_dsut(trip_I, day_start_ut):
            return events

        query = """SELECT stop_I, arr_time_ds+?, dep_time_ds+?
                    FROM stop_times JOIN stops USING(stop_I)
                    WHERE
                        (trip_I = ?)
                """
        params = [day_start_ut, day_start_ut,
                  trip_I]
        if start_ut:
            query += "AND (dep_time_ds > ?-?)"
            params += [start_ut, day_start_ut]
        if end_ut:
            query += "AND (arr_time_ds < ?-?)"
            params += [end_ut, day_start_ut]
        query += "ORDER BY arr_time_ds"
        cur = self.conn.cursor()
        rows = cur.execute(query, params)
        stop_data = list(rows)
        for i in range(len(stop_data) - 1):
            event = {
                "from_stop": stop_data[i][0],
                "to_stop": stop_data[i + 1][0],
                "dep_time_ut": stop_data[i][2],
                "arr_time_ut": stop_data[i + 1][1]
            }
            events.append(event)
        return events