def _journey_label_generator(self, destination_stop_Is=None, origin_stop_Is=None):
        """
        Parameters
        ----------
        destination_stop_Is: list-like
        origin_stop_Is: list-like

        Yields
        ------
        (origin_stop_I, destination_stop_I, journey_labels) : tuple
        """
        conn = self.conn
        conn.row_factory = sqlite3.Row
        if destination_stop_Is is None:
            destination_stop_Is = self.get_targets_having_journeys()
        if origin_stop_Is is None:
            origin_stop_Is = self.get_origins_having_journeys()

        for destination_stop_I in destination_stop_Is:
            if self.track_route:
                label_features = "journey_id, from_stop_I, to_stop_I, n_boardings, movement_duration, " \
                                 "journey_duration, in_vehicle_duration, transfer_wait_duration, walking_duration, " \
                                 "departure_time, arrival_time_target"""
            else:
                label_features = "journey_id, from_stop_I, to_stop_I, n_boardings, departure_time, " \
                                 "arrival_time_target"
            sql = "SELECT " + label_features + " FROM journeys WHERE to_stop_I = %s" % destination_stop_I

            df = pd.read_sql_query(sql, self.conn)
            for origin_stop_I in origin_stop_Is:
                selection = df.loc[df['from_stop_I'] == origin_stop_I]
                journey_labels = []
                for journey in selection.to_dict(orient='records'):
                    journey["pre_journey_wait_fp"] = -1
                    try:
                        journey_labels.append(LabelGeneric(journey))
                    except Exception as e:
                        print(journey)
                        raise e
                yield origin_stop_I, destination_stop_I, journey_labels