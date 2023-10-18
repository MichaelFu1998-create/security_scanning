def get_route_name_and_type_of_tripI(self, trip_I):
        """
        Get route short name and type

        Parameters
        ----------
        trip_I: int
            short trip index created when creating the database

        Returns
        -------
        name: str
            short name of the route, eg. 195N
        type: int
            route_type according to the GTFS standard
        """
        cur = self.conn.cursor()
        results = cur.execute("SELECT name, type FROM routes JOIN trips USING(route_I) WHERE trip_I={trip_I}"
                              .format(trip_I=trip_I))
        name, rtype = results.fetchone()
        return u"%s" % str(name), int(rtype)