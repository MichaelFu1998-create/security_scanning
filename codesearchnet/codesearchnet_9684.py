def _filter_by_calendar(self):
        """
        update calendar table's services
        :param copy_db_conn:
        :param start_date:
        :param end_date:
        :return:
        """
        if (self.start_date is not None) and (self.end_date is not None):
            logging.info("Making date extract")

            start_date_query = "UPDATE calendar " \
                               "SET start_date='{start_date}' " \
                               "WHERE start_date<'{start_date}' ".format(start_date=self.start_date)
            self.copy_db_conn.execute(start_date_query)

            end_date_query = "UPDATE calendar " \
                             "SET end_date='{end_date_to_include}' " \
                             "WHERE end_date>'{end_date_to_include}' " \
                .format(end_date_to_include=self.end_date_to_include_str)
            self.copy_db_conn.execute(end_date_query)

            # then recursively delete further data:
            self.copy_db_conn.execute(DELETE_TRIPS_NOT_IN_DAYS_SQL)
            self.copy_db_conn.execute(DELETE_SHAPES_NOT_REFERENCED_IN_TRIPS_SQL)
            self.copy_db_conn.execute(DELETE_STOP_TIMES_NOT_REFERENCED_IN_TRIPS_SQL)
            delete_stops_not_in_stop_times_and_not_as_parent_stop(self.copy_db_conn)
            self.copy_db_conn.execute(DELETE_STOP_DISTANCE_ENTRIES_WITH_NONEXISTENT_STOPS_SQL)
            self.copy_db_conn.execute(DELETE_ROUTES_NOT_PRESENT_IN_TRIPS_SQL)
            self.copy_db_conn.execute(DELETE_AGENCIES_NOT_REFERENCED_IN_ROUTES_SQL)
            self.copy_db_conn.commit()
            return FILTERED
        else:
            return NOT_FILTERED