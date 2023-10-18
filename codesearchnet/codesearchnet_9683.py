def _delete_rows_by_start_and_end_date(self):
        """
        Removes rows from the sqlite database copy that are out of the time span defined by start_date and end_date
        :param gtfs: GTFS object
        :param copy_db_conn: sqlite database connection
        :param start_date:
        :param end_date:
        :return:
        """
        # filter by start_time_ut and end_date_ut:
        if (self.start_date is not None) and (self.end_date is not None):
            start_date_ut = self.gtfs.get_day_start_ut(self.start_date)
            end_date_ut = self.gtfs.get_day_start_ut(self.end_date)
            if self.copy_db_conn.execute("SELECT count(*) FROM day_trips2 WHERE start_time_ut IS null "
                                         "OR end_time_ut IS null").fetchone() != (0,):
                raise ValueError("Missing information in day_trips2 (start_time_ut and/or end_time_ut), "
                                 "check trips.start_time_ds and trips.end_time_ds.")
            logging.info("Filtering based on start_time_ut and end_time_ut")
            table_to_preserve_map = {
                "calendar": "start_date < date({filter_end_ut}, 'unixepoch', 'localtime') "
                            "AND "
                            "end_date >= date({filter_start_ut}, 'unixepoch', 'localtime') ",
                "calendar_dates": "date >= date({filter_start_ut}, 'unixepoch', 'localtime') "
                                  "AND "
                                  "date < date({filter_end_ut}, 'unixepoch', 'localtime') ",
                "day_trips2": 'start_time_ut < {filter_end_ut} '
                              'AND '
                              'end_time_ut > {filter_start_ut} ',
                "days": "day_start_ut >= {filter_start_ut} "
                        "AND "
                        "day_start_ut < {filter_end_ut} "
                }
            table_to_remove_map = {key: "WHERE NOT ( " + to_preserve + " );"
                                   for key, to_preserve in table_to_preserve_map.items() }

            # Ensure that process timezone is correct as we rely on 'localtime' in the SQL statements.
            GTFS(self.copy_db_conn).set_current_process_time_zone()
            # remove the 'source' entries from tables
            for table, query_template in table_to_remove_map.items():
                param_dict = {"filter_start_ut": str(start_date_ut),
                              "filter_end_ut": str(end_date_ut)}
                query = "DELETE FROM " + table + " " + \
                        query_template.format(**param_dict)
                self.copy_db_conn.execute(query)
                self.copy_db_conn.commit()

            return FILTERED
        else:
            return NOT_FILTERED