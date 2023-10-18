def _validate_table_row_counts(self):
        """
        Imports source .txt files, checks row counts and then compares the rowcounts with the gtfsobject
        :return:
        """
        for db_table_name in DB_TABLE_NAME_TO_SOURCE_FILE.keys():
            table_name_source_file = DB_TABLE_NAME_TO_SOURCE_FILE[db_table_name]
            row_warning_str = DB_TABLE_NAME_TO_ROWS_MISSING_WARNING[db_table_name]

            # Row count in GTFS object:
            database_row_count = self.gtfs.get_row_count(db_table_name)

            # Row counts in source files:
            source_row_count = 0
            for gtfs_source in self.gtfs_sources:
                frequencies_in_source = source_csv_to_pandas(gtfs_source, 'frequencies.txt')
                try:
                    if table_name_source_file == 'trips' and not frequencies_in_source.empty:
                        source_row_count += self._frequency_generated_trips_rows(gtfs_source)

                    elif table_name_source_file == 'stop_times' and not frequencies_in_source.empty:
                        source_row_count += self._compute_number_of_frequency_generated_stop_times(gtfs_source)
                    else:
                        df = source_csv_to_pandas(gtfs_source, table_name_source_file)

                        source_row_count += len(df.index)
                except IOError as e:
                    if hasattr(e, "filename") and db_table_name in e.filename:
                        pass
                    else:
                        raise e


            if source_row_count == database_row_count and self.verbose:
                print("Row counts match for " + table_name_source_file + " between the source and database ("
                      + str(database_row_count) + ")")
            else:
                difference = database_row_count - source_row_count
                ('Row counts do not match for ' + str(table_name_source_file) + ': (source=' + str(source_row_count) +
                      ', database=' + str(database_row_count) + ")")
                if table_name_source_file == "calendar" and difference > 0:
                    query = "SELECT count(*) FROM (SELECT * FROM calendar ORDER BY service_I DESC LIMIT " \
                            + str(int(difference)) + \
                            ") WHERE start_date=end_date AND m=0 AND t=0 AND w=0 AND th=0 AND f=0 AND s=0 AND su=0"
                    number_of_entries_added_by_calendar_dates_loader = self.gtfs.execute_custom_query(query).fetchone()[
                        0]
                    if number_of_entries_added_by_calendar_dates_loader == difference and self.verbose:
                        print("    But don't worry, the extra entries seem to just dummy entries due to calendar_dates")
                    else:
                        if self.verbose:
                            print("    Reason for this is unknown.")
                        self.warnings_container.add_warning(row_warning_str, self.location, difference)
                else:
                    self.warnings_container.add_warning(row_warning_str, self.location, difference)