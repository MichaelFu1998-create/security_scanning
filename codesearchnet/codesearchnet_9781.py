def get_tripIs_active_in_range(self, start, end):
        """
        Obtain from the (standard) GTFS database, list of trip_IDs (and other trip_related info)
        that are active between given 'start' and 'end' times.

        The start time of a trip is determined by the departure time at the last stop of the trip.
        The end time of a trip is determined by the arrival time at the last stop of the trip.

        Parameters
        ----------
        start, end : int
            the start and end of the time interval in unix time seconds

        Returns
        -------
        active_trips : pandas.DataFrame with columns
            trip_I, day_start_ut, start_time_ut, end_time_ut, shape_id
        """
        to_select = "trip_I, day_start_ut, start_time_ut, end_time_ut, shape_id "
        query = "SELECT " + to_select + \
                "FROM day_trips " \
                "WHERE " \
                "(end_time_ut > {start_ut} AND start_time_ut < {end_ut})".format(start_ut=start, end_ut=end)
        return pd.read_sql_query(query, self.conn)