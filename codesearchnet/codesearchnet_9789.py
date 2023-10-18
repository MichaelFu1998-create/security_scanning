def get_trip_stop_coordinates(self, trip_I):
        """
        Get coordinates for a given trip_I

        Parameters
        ----------
        trip_I : int
            the integer id of the trip

        Returns
        -------
        stop_coords : pandas.DataFrame
            with columns "lats" and "lons"
        """
        query = """SELECT lat, lon
                    FROM stop_times
                    JOIN stops
                    USING(stop_I)
                        WHERE trip_I={trip_I}
                    ORDER BY stop_times.seq""".format(trip_I=trip_I)
        stop_coords = pd.read_sql(query, self.conn)
        return stop_coords