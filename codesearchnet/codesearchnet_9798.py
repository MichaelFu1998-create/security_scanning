def get_stops_for_route_type(self, route_type):
        """
        Parameters
        ----------
        route_type: int

        Returns
        -------
        stops: pandas.DataFrame

        """
        if route_type is WALK:
            return self.stops()
        else:
            return pd.read_sql_query("SELECT DISTINCT stops.* "
                                     "FROM stops JOIN stop_times ON stops.stop_I == stop_times.stop_I "
                                     "           JOIN trips ON stop_times.trip_I = trips.trip_I"
                                     "           JOIN routes ON trips.route_I == routes.route_I "
                                     "WHERE routes.type=(?)", self.conn, params=(route_type,))