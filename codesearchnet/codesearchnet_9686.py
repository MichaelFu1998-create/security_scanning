def _filter_spatially(self):
        """
        Filter the feed based on self.buffer_distance_km from self.buffer_lon and self.buffer_lat.

        1. First include all stops that are within self.buffer_distance_km from self.buffer_lon and self.buffer_lat.
        2. Then include all intermediate stops that are between any of the included stop pairs with some PT trip.
        3. Repeat step 2 until no more stops are to be included.

        As a summary this process should get rid of PT network tendrils, but should preserve the PT network intact
        at its core.
        """
        if self.buffer_lat is None or self.buffer_lon is None or self.buffer_distance_km is None:
            return NOT_FILTERED

        print("filtering with lat: " + str(self.buffer_lat) +
              " lon: " + str(self.buffer_lon) +
              " buffer distance: " + str(self.buffer_distance_km))
        remove_all_trips_fully_outside_buffer(self.copy_db_conn,
                                              self.buffer_lat,
                                              self.buffer_lon,
                                              self.buffer_distance_km,
                                              update_secondary_data=False)
        logging.info("Making spatial extract")

        find_distance_func_name = add_wgs84_distance_function_to_db(self.copy_db_conn)
        assert find_distance_func_name == "find_distance"

        # select all stops that are within the buffer and have some stop_times assigned.
        stop_distance_filter_sql_base = (
            "SELECT DISTINCT stops.stop_I FROM stops, stop_times" +
            "    WHERE CAST(find_distance(lat, lon, {buffer_lat}, {buffer_lon}) AS INT) < {buffer_distance_meters}" +
            "     AND stops.stop_I=stop_times.stop_I"
        )
        stops_within_buffer_sql = stop_distance_filter_sql_base.format(
            buffer_lat=float(self.buffer_lat),
            buffer_lon=float(self.buffer_lon),
            buffer_distance_meters=int(self.buffer_distance_km * 1000)
        )
        stops_within_buffer = set(row[0] for row in self.copy_db_conn.execute(stops_within_buffer_sql))

        # For each trip_I, find smallest (min_seq) and largest (max_seq) stop sequence numbers that
        # are within the soft buffer_distance from the buffer_lon and buffer_lat, and add them into the
        # list of stops to preserve.
        # Note that if a trip is OUT-IN-OUT-IN-OUT, this process preserves (at least) the part IN-OUT-IN of the trip.
        # Repeat until no more stops are found.

        stops_within_buffer_string = "(" +",".join(str(stop_I) for stop_I in stops_within_buffer) +  ")"
        trip_min_max_include_seq_sql =  (
            'SELECT trip_I, min(seq) AS min_seq, max(seq) AS max_seq FROM stop_times, stops '
                    'WHERE stop_times.stop_I = stops.stop_I '
                    ' AND stops.stop_I IN {stop_I_list}'
                    ' GROUP BY trip_I'
        ).format(stop_I_list=stops_within_buffer_string)
        trip_I_min_seq_max_seq_df = pandas.read_sql(trip_min_max_include_seq_sql, self.copy_db_conn)

        for trip_I_seq_row in trip_I_min_seq_max_seq_df.itertuples():
            trip_I = trip_I_seq_row.trip_I
            min_seq = trip_I_seq_row.min_seq
            max_seq = trip_I_seq_row.max_seq
            # DELETE FROM STOP_TIMES
            if min_seq == max_seq:
                # Only one entry in stop_times to be left, remove whole trip.
                self.copy_db_conn.execute("DELETE FROM stop_times WHERE trip_I={trip_I}".format(trip_I=trip_I))
                self.copy_db_conn.execute("DELETE FROM trips WHERE trip_i={trip_I}".format(trip_I=trip_I))
            else:
                # DELETE STOP_TIME ENTRIES BEFORE ENTERING AND AFTER DEPARTING THE BUFFER AREA
                DELETE_STOP_TIME_ENTRIES_SQL = \
                    "DELETE FROM stop_times WHERE trip_I={trip_I} AND (seq<{min_seq} OR seq>{max_seq})"\
                    .format(trip_I=trip_I, max_seq=max_seq, min_seq=min_seq)
                self.copy_db_conn.execute(DELETE_STOP_TIME_ENTRIES_SQL)

                STOPS_NOT_WITHIN_BUFFER__FOR_TRIP_SQL = \
                    "SELECT seq, stop_I IN {stops_within_hard_buffer} AS within FROM stop_times WHERE trip_I={trip_I} ORDER BY seq"\
                    .format(stops_within_hard_buffer=stops_within_buffer_string, trip_I=trip_I)
                stop_times_within_buffer_df = pandas.read_sql(STOPS_NOT_WITHIN_BUFFER__FOR_TRIP_SQL, self.copy_db_conn)
                if stop_times_within_buffer_df['within'].all():
                    continue
                else:
                    _split_trip(self.copy_db_conn, trip_I, stop_times_within_buffer_df)


        # Delete all shapes that are not fully within the buffer to avoid shapes going outside
        # the buffer area in a some cases.
        # This could probably be done in some more sophisticated way though (per trip)
        SHAPE_IDS_NOT_WITHIN_BUFFER_SQL = \
            "SELECT DISTINCT shape_id FROM SHAPES " \
            "WHERE CAST(find_distance(lat, lon, {buffer_lat}, {buffer_lon}) AS INT) > {buffer_distance_meters}" \
            .format(buffer_lat=self.buffer_lat,
                    buffer_lon=self.buffer_lon,
                    buffer_distance_meters=self.buffer_distance_km * 1000)
        DELETE_ALL_SHAPE_IDS_NOT_WITHIN_BUFFER_SQL = "DELETE FROM shapes WHERE shape_id IN (" \
                                                          + SHAPE_IDS_NOT_WITHIN_BUFFER_SQL + ")"
        self.copy_db_conn.execute(DELETE_ALL_SHAPE_IDS_NOT_WITHIN_BUFFER_SQL)
        SET_SHAPE_ID_TO_NULL_FOR_HARD_BUFFER_FILTERED_SHAPE_IDS = \
            "UPDATE trips SET shape_id=NULL WHERE trips.shape_id IN (" + SHAPE_IDS_NOT_WITHIN_BUFFER_SQL + ")"
        self.copy_db_conn.execute(SET_SHAPE_ID_TO_NULL_FOR_HARD_BUFFER_FILTERED_SHAPE_IDS)


        # Delete trips with only one stop
        self.copy_db_conn.execute('DELETE FROM stop_times WHERE '
                                  'trip_I IN (SELECT trip_I FROM '
                                  '(SELECT trip_I, count(*) AS N_stops from stop_times '
                                  'GROUP BY trip_I) q1 '
                                  'WHERE N_stops = 1)')

        # Delete trips with only one stop but several instances in stop_times
        self.copy_db_conn.execute('DELETE FROM stop_times WHERE '
                                  'trip_I IN (SELECT q1.trip_I AS trip_I FROM '
                                    '(SELECT trip_I, stop_I, count(*) AS stops_per_stop FROM stop_times '
                                    'GROUP BY trip_I, stop_I) q1, '
                                    '(SELECT trip_I, count(*) as n_stops FROM stop_times '
                                    'GROUP BY trip_I) q2 '
                                    'WHERE q1.trip_I = q2.trip_I AND n_stops = stops_per_stop)')

        # Delete all stop_times for uncovered stops
        delete_stops_not_in_stop_times_and_not_as_parent_stop(self.copy_db_conn)
        # Consecutively delete all the rest remaining.
        self.copy_db_conn.execute(DELETE_TRIPS_NOT_REFERENCED_IN_STOP_TIMES)
        self.copy_db_conn.execute(DELETE_ROUTES_NOT_PRESENT_IN_TRIPS_SQL)
        self.copy_db_conn.execute(DELETE_AGENCIES_NOT_REFERENCED_IN_ROUTES_SQL)
        self.copy_db_conn.execute(DELETE_SHAPES_NOT_REFERENCED_IN_TRIPS_SQL)
        self.copy_db_conn.execute(DELETE_STOP_DISTANCE_ENTRIES_WITH_NONEXISTENT_STOPS_SQL)
        self.copy_db_conn.execute(DELETE_FREQUENCIES_ENTRIES_NOT_PRESENT_IN_TRIPS)
        remove_dangling_shapes(self.copy_db_conn)
        self.copy_db_conn.commit()
        return FILTERED