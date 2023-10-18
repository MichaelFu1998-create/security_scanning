def _filter_by_agency(self):
        """
        filter by agency ids
        :param copy_db_conn:
        :param agency_ids_to_preserve:
        :return:
        """
        if self.agency_ids_to_preserve is not None:
            logging.info("Filtering based on agency_ids")
            agency_ids_to_preserve = list(self.agency_ids_to_preserve)
            agencies = pandas.read_sql("SELECT * FROM agencies", self.copy_db_conn)
            agencies_to_remove = []
            for idx, row in agencies.iterrows():
                if row['agency_id'] not in agency_ids_to_preserve:
                    agencies_to_remove.append(row['agency_id'])
            for agency_id in agencies_to_remove:
                self.copy_db_conn.execute('DELETE FROM agencies WHERE agency_id=?', (agency_id,))
            # and remove recursively related to the agencies:
            self.copy_db_conn.execute('DELETE FROM routes WHERE '
                                      'agency_I NOT IN (SELECT agency_I FROM agencies)')
            self.copy_db_conn.execute('DELETE FROM trips WHERE '
                                      'route_I NOT IN (SELECT route_I FROM routes)')
            self.copy_db_conn.execute('DELETE FROM calendar WHERE '
                                      'service_I NOT IN (SELECT service_I FROM trips)')
            self.copy_db_conn.execute('DELETE FROM calendar_dates WHERE '
                                      'service_I NOT IN (SELECT service_I FROM trips)')
            self.copy_db_conn.execute('DELETE FROM days WHERE '
                                      'trip_I NOT IN (SELECT trip_I FROM trips)')
            self.copy_db_conn.execute('DELETE FROM stop_times WHERE '
                                      'trip_I NOT IN (SELECT trip_I FROM trips)')
            self.copy_db_conn.execute('DELETE FROM stop_times WHERE '
                                      'trip_I NOT IN (SELECT trip_I FROM trips)')
            self.copy_db_conn.execute('DELETE FROM shapes WHERE '
                                      'shape_id NOT IN (SELECT shape_id FROM trips)')
            self.copy_db_conn.execute('DELETE FROM day_trips2 WHERE '
                                      'trip_I NOT IN (SELECT trip_I FROM trips)')
            self.copy_db_conn.commit()
            return FILTERED
        else:
            return NOT_FILTERED