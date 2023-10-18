def get_all_route_shapes(self, use_shapes=True):
        """
        Get the shapes of all routes.

        Parameters
        ----------
        use_shapes : bool, optional
            by default True (i.e. use shapes as the name of the function indicates)
            if False (fall back to lats and longitudes)

        Returns
        -------
        routeShapes: list of dicts that should have the following keys
            name, type, agency, lats, lons
            with types
            list, list, str, list, list
        """
        cur = self.conn.cursor()

        # all shape_id:s corresponding to a route_I:
        # query = "SELECT DISTINCT name, shape_id, trips.route_I, route_type
        #          FROM trips LEFT JOIN routes USING(route_I)"
        # data1 = pd.read_sql_query(query, self.conn)
        # one (arbitrary) shape_id per route_I ("one direction") -> less than half of the routes
        query = "SELECT routes.name as name, shape_id, route_I, trip_I, routes.type, " \
                "        agency_id, agencies.name as agency_name, max(end_time_ds-start_time_ds) as trip_duration " \
                "FROM trips " \
                "LEFT JOIN routes " \
                "USING(route_I) " \
                "LEFT JOIN agencies " \
                "USING(agency_I) " \
                "GROUP BY routes.route_I"
        data = pd.read_sql_query(query, self.conn)

        routeShapes = []
        for i, row in enumerate(data.itertuples()):
            datum = {"name": str(row.name), "type": int(row.type), "route_I": row.route_I, "agency": str(row.agency_id),
                     "agency_name": str(row.agency_name)}
            # this function should be made also non-shape friendly (at this point)
            if use_shapes and row.shape_id:
                shape = shapes.get_shape_points2(cur, row.shape_id)
                lats = shape['lats']
                lons = shape['lons']
            else:
                stop_shape = self.get_trip_stop_coordinates(row.trip_I)
                lats = list(stop_shape['lat'])
                lons = list(stop_shape['lon'])
            datum['lats'] = [float(lat) for lat in lats]
            datum['lons'] = [float(lon) for lon in lons]
            routeShapes.append(datum)
        return routeShapes