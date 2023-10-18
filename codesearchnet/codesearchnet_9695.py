def _insert_journeys_into_db_no_route(self, stop_profiles, target_stop=None):
        # TODO: Change the insertion so that the check last journey id and insertions are in the same transaction block
        """
        con.isolation_level = 'EXCLUSIVE'
        con.execute('BEGIN EXCLUSIVE')
        #exclusive access starts here. Nothing else can r/w the db, do your magic here.
        con.commit()
        """
        print("Collecting journey data")
        journey_id = 1
        journey_list = []
        tot = len(stop_profiles)
        for i, (origin_stop, labels) in enumerate(stop_profiles.items(), start=1):
            #print("\r Stop " + str(i) + " of " + str(tot), end='', flush=True)
            for label in labels:
                assert (isinstance(label, LabelTimeWithBoardingsCount))
                if self.multitarget_routing:
                    target_stop = None
                else:
                    target_stop = int(target_stop)

                values = [int(journey_id),
                          int(origin_stop),
                          target_stop,
                          int(label.departure_time),
                          int(label.arrival_time_target),
                          int(label.n_boardings)]

                journey_list.append(values)
                journey_id += 1
        print("Inserting journeys without route into database")
        insert_journeys_stmt = '''INSERT INTO journeys(
              journey_id,
              from_stop_I,
              to_stop_I,
              departure_time,
              arrival_time_target,
              n_boardings) VALUES (%s) ''' % (", ".join(["?" for x in range(6)]))
        #self.conn.executemany(insert_journeys_stmt, journey_list)
        self._executemany_exclusive(insert_journeys_stmt, journey_list)
        self.conn.commit()