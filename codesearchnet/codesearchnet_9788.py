def get_route_name_and_type(self, route_I):
        """
        Get route short name and type

        Parameters
        ----------
        route_I: int
            route index (database specific)

        Returns
        -------
        name: str
            short name of the route, eg. 195N
        type: int
            route_type according to the GTFS standard
        """
        cur = self.conn.cursor()
        results = cur.execute("SELECT name, type FROM routes WHERE route_I=(?)", (route_I,))
        name, rtype = results.fetchone()
        return name, int(rtype)