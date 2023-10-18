def import_journey_data_for_target_stop(self, target_stop_I, origin_stop_I_to_journey_labels, enforce_synchronous_writes=False):
        """
        Parameters
        ----------
        origin_stop_I_to_journey_labels: dict
            key: origin_stop_Is
            value: list of labels
        target_stop_I: int
        """
        cur = self.conn.cursor()
        self.conn.isolation_level = 'EXCLUSIVE'
        # if not enforce_synchronous_writes:
        cur.execute('PRAGMA synchronous = 0;')

        if self.track_route:
            self._insert_journeys_with_route_into_db(origin_stop_I_to_journey_labels, target_stop=int(target_stop_I))
        else:
            self._insert_journeys_into_db_no_route(origin_stop_I_to_journey_labels, target_stop=int(target_stop_I))
        print("Finished import process")
        self.conn.commit()