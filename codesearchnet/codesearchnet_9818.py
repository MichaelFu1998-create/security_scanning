def get_journey_legs_to_target(self, target, fastest_path=True, min_boardings=False, all_leg_sections=True,
                                                   ignore_walk=False, diff_threshold=None, diff_path=None):
        """
        Returns a dataframe of aggregated sections from source nodes to target. The returned sections are either
        transfer point to transfer point or stop to stop. In a before after setting, the results can be filtered based
        on values in a difference db.
        :param target:
        :param fastest_path:
        :param min_boardings:
        :param all_leg_sections:
        :param ignore_walk:
        :param diff_threshold:
        :param diff_path:
        :return:
        """
        assert not (fastest_path and min_boardings)
        if min_boardings:
            raise NotImplementedError
        if all_leg_sections and diff_threshold:
            raise NotImplementedError

        added_constraints = ""
        add_diff = ""
        if fastest_path:
            added_constraints += " AND journeys.pre_journey_wait_fp>=0"
        if ignore_walk:
            added_constraints += " AND legs.trip_I >= 0"
        if diff_path and diff_threshold:
            self.conn = attach_database(self.conn, diff_path, name="diff")
            add_diff = ", diff.diff_temporal_distance"
            added_constraints += " AND abs(diff_temporal_distance.diff_mean) >= %s " \
                                 "AND diff_temporal_distance.from_stop_I = journeys.from_stop_I " \
                                 "AND diff_temporal_distance.to_stop_I = journeys.to_stop_I" % (diff_threshold,)

        if all_leg_sections:
            df = self._get_journey_legs_to_target_with_all_sections(target, added_constraints)
        else:
            query = """SELECT from_stop_I, to_stop_I, coalesce(type, -1) AS type,
                         count(*) AS n_trips
                         FROM
                         (SELECT legs.* FROM legs, journeys %s
                         WHERE journeys.journey_id = legs.journey_id AND journeys.to_stop_I = %s %s) q1
                         LEFT JOIN (SELECT * FROM other.trips, other.routes WHERE trips.route_I = routes.route_I) q2
                         ON q1.trip_I = q2.trip_I
                         GROUP BY from_stop_I, to_stop_I, type""" % (add_diff, str(target), added_constraints)
            df = read_sql_query(query, self.conn)

        return df