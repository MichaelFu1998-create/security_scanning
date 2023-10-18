def validate_and_get_warnings(self):
        """
        Validates/checks a given GTFS feed with respect to a number of different issues.

        The set of warnings that are checked for, can be found in the gtfs_validator.ALL_WARNINGS

        Returns
        -------
        warnings: WarningsContainer
        """
        self.warnings_container.clear()
        self._validate_stops_with_same_stop_time()
        self._validate_speeds_and_trip_times()
        self._validate_stop_spacings()
        self._validate_stop_sequence()
        self._validate_misplaced_stops()
        return self.warnings_container