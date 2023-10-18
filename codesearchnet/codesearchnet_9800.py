def get_transit_events(self, start_time_ut=None, end_time_ut=None, route_type=None):
        """
        Obtain a list of events that take place during a time interval.
        Each event needs to be only partially overlap the given time interval.
        Does not include walking events.

        Parameters
        ----------
        start_time_ut : int
            start of the time interval in unix time (seconds)
        end_time_ut: int
            end of the time interval in unix time (seconds)
        route_type: int
            consider only events for this route_type

        Returns
        -------
        events: pandas.DataFrame
            with the following columns and types
                dep_time_ut: int
                arr_time_ut: int
                from_stop_I: int
                to_stop_I: int
                trip_I : int
                shape_id : int
                route_type : int

        See also
        --------
        get_transit_events_in_time_span : an older version of the same thing
        """
        table_name = self._get_day_trips_table_name()
        event_query = "SELECT stop_I, seq, trip_I, route_I, routes.route_id AS route_id, routes.type AS route_type, " \
                      "shape_id, day_start_ut+dep_time_ds AS dep_time_ut, day_start_ut+arr_time_ds AS arr_time_ut " \
                      "FROM " + table_name + " " \
                                             "JOIN trips USING(trip_I) " \
                                             "JOIN routes USING(route_I) " \
                                             "JOIN stop_times USING(trip_I)"

        where_clauses = []
        if end_time_ut:
            where_clauses.append(table_name + ".start_time_ut< {end_time_ut}".format(end_time_ut=end_time_ut))
            where_clauses.append("dep_time_ut  <={end_time_ut}".format(end_time_ut=end_time_ut))
        if start_time_ut:
            where_clauses.append(table_name + ".end_time_ut  > {start_time_ut}".format(start_time_ut=start_time_ut))
            where_clauses.append("arr_time_ut  >={start_time_ut}".format(start_time_ut=start_time_ut))
        if route_type is not None:
            assert route_type in ALL_ROUTE_TYPES
            where_clauses.append("routes.type={route_type}".format(route_type=route_type))
        if len(where_clauses) > 0:
            event_query += " WHERE "
            for i, where_clause in enumerate(where_clauses):
                if i is not 0:
                    event_query += " AND "
                event_query += where_clause
        # ordering is required for later stages
        event_query += " ORDER BY trip_I, day_start_ut+dep_time_ds;"
        events_result = pd.read_sql_query(event_query, self.conn)
        # 'filter' results so that only real "events" are taken into account
        from_indices = numpy.nonzero(
            (events_result['trip_I'][:-1].values == events_result['trip_I'][1:].values) *
            (events_result['seq'][:-1].values < events_result['seq'][1:].values)
        )[0]
        to_indices = from_indices + 1
        # these should have same trip_ids
        assert (events_result['trip_I'][from_indices].values == events_result['trip_I'][to_indices].values).all()
        trip_Is = events_result['trip_I'][from_indices]
        from_stops = events_result['stop_I'][from_indices]
        to_stops = events_result['stop_I'][to_indices]
        shape_ids = events_result['shape_id'][from_indices]
        dep_times = events_result['dep_time_ut'][from_indices]
        arr_times = events_result['arr_time_ut'][to_indices]
        route_types = events_result['route_type'][from_indices]
        route_ids = events_result['route_id'][from_indices]
        route_Is = events_result['route_I'][from_indices]
        durations = arr_times.values - dep_times.values
        assert (durations >= 0).all()
        from_seqs = events_result['seq'][from_indices]
        to_seqs = events_result['seq'][to_indices]
        data_tuples = zip(from_stops, to_stops, dep_times, arr_times,
                          shape_ids, route_types, route_ids, trip_Is,
                          durations, from_seqs, to_seqs, route_Is)
        columns = ["from_stop_I", "to_stop_I", "dep_time_ut", "arr_time_ut",
                   "shape_id", "route_type", "route_id", "trip_I",
                   "duration", "from_seq", "to_seq", "route_I"]
        df = pd.DataFrame.from_records(data_tuples, columns=columns)
        return df