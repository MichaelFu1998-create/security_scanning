def _validate_danglers(self):
        """
        Checks for rows that are not referenced in the the tables that should be linked

        stops <> stop_times using stop_I
        stop_times <> trips <> days, using trip_I
        trips <> routes, using route_I
        :return:
        """
        for query, warning in zip(DANGLER_QUERIES, DANGLER_WARNINGS):
            dangler_count = self.gtfs.execute_custom_query(query).fetchone()[0]
            if dangler_count > 0:
                if self.verbose:
                    print(str(dangler_count) + " " + warning)
                self.warnings_container.add_warning(warning, self.location, count=dangler_count)