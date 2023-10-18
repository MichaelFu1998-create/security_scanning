def get_trip_stop_time_data(self, trip_I, day_start_ut):
        """
        Obtain from the (standard) GTFS database, trip stop data
        (departure time in ut, lat, lon, seq, shape_break) as a pandas DataFrame

        Some filtering could be applied here, if only e.g. departure times
        corresponding within some time interval should be considered.

        Parameters
        ----------
        trip_I : int
            integer index of the trip
        day_start_ut : int
            the start time of the day in unix time (seconds)

        Returns
        -------
        df: pandas.DataFrame
            df has the following columns
            'departure_time_ut, lat, lon, seq, shape_break'
        """
        to_select = "stop_I, " + str(day_start_ut) + "+dep_time_ds AS dep_time_ut, lat, lon, seq, shape_break"
        str_to_run = "SELECT " + to_select + """
                        FROM stop_times JOIN stops USING(stop_I)
                        WHERE (trip_I ={trip_I}) ORDER BY seq
                      """
        str_to_run = str_to_run.format(trip_I=trip_I)
        return pd.read_sql_query(str_to_run, self.conn)