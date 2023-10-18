def get_trip_trajectories_within_timespan(self, start, end, use_shapes=True, filter_name=None):
        """
        Get complete trip data for visualizing public transport operation based on gtfs.

        Parameters
        ----------
        start: number
            Earliest position data to return (in unix time)
        end: number
            Latest position data to return (in unix time)
        use_shapes: bool, optional
            Whether or not shapes should be included
        filter_name: str
            Pick only routes having this name.

        Returns
        -------
        trips: dict
            trips['trips'] is a list whose each element (e.g. el = trips['trips'][0])
            is a dict with the following properties:
                el['lats'] -- list of latitudes
                el['lons'] -- list of longitudes
                el['times'] -- list of passage_times
                el['route_type'] -- type of vehicle as specified by GTFS
                el['name'] -- name of the route
        """
        trips = []
        trip_df = self.get_tripIs_active_in_range(start, end)
        print("gtfs_viz.py: fetched " + str(len(trip_df)) + " trip ids")
        shape_cache = {}

        # loop over all trips:
        for row in trip_df.itertuples():
            trip_I = row.trip_I
            day_start_ut = row.day_start_ut
            shape_id = row.shape_id

            trip = {}

            name, route_type = self.get_route_name_and_type_of_tripI(trip_I)
            trip['route_type'] = int(route_type)
            trip['name'] = str(name)

            if filter_name and (name != filter_name):
                continue

            stop_lats = []
            stop_lons = []
            stop_dep_times = []
            shape_breaks = []
            stop_seqs = []

            # get stop_data and store it:
            stop_time_df = self.get_trip_stop_time_data(trip_I, day_start_ut)
            for stop_row in stop_time_df.itertuples():
                stop_lats.append(float(stop_row.lat))
                stop_lons.append(float(stop_row.lon))
                stop_dep_times.append(float(stop_row.dep_time_ut))
                try:
                    stop_seqs.append(int(stop_row.seq))
                except TypeError:
                    stop_seqs.append(None)
                if use_shapes:
                    try:
                        shape_breaks.append(int(stop_row.shape_break))
                    except (TypeError, ValueError):
                        shape_breaks.append(None)

            if use_shapes:
                # get shape data (from cache, if possible)
                if shape_id not in shape_cache:
                    shape_cache[shape_id] = shapes.get_shape_points2(self.conn.cursor(), shape_id)
                shape_data = shape_cache[shape_id]
                # noinspection PyBroadException
                try:
                    trip['times'] = shapes.interpolate_shape_times(shape_data['d'], shape_breaks, stop_dep_times)
                    trip['lats'] = shape_data['lats']
                    trip['lons'] = shape_data['lons']
                    start_break = shape_breaks[0]
                    end_break = shape_breaks[-1]
                    trip['times'] = trip['times'][start_break:end_break + 1]
                    trip['lats'] = trip['lats'][start_break:end_break + 1]
                    trip['lons'] = trip['lons'][start_break:end_break + 1]
                except:
                    # In case interpolation fails:
                    trip['times'] = stop_dep_times
                    trip['lats'] = stop_lats
                    trip['lons'] = stop_lons
            else:
                trip['times'] = stop_dep_times
                trip['lats'] = stop_lats
                trip['lons'] = stop_lons
            trips.append(trip)
        return {"trips": trips}