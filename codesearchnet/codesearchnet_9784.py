def get_weekly_extract_start_date(self, ut=False, weekdays_at_least_of_max=0.9,
                                      verbose=False, download_date_override=None):
        """
        Find a suitable weekly extract start date (monday).
        The goal is to obtain as 'usual' week as possible.
        The weekdays of the weekly extract week should contain
        at least 0.9 of the total maximum of trips.

        Parameters
        ----------
        ut: return unixtime?
        weekdays_at_least_of_max: float

        download_date_override: str, semi-optional
            Download-date in format %Y-%m-%d, weeks close to this.
            Overrides the (possibly) recorded downloaded date in the database

        Returns
        -------
        date: int or str

        Raises
        ------
        error: RuntimeError
            If no download date could be found.
        """
        daily_trip_counts = self.get_trip_counts_per_day()
        if isinstance(download_date_override, str):
            search_start_date = datetime.datetime.strptime(download_date_override, "%Y-%m-%d")
        elif isinstance(download_date_override, datetime.datetime):
            search_start_date = download_date_override
        else:
            assert download_date_override is None
            download_date_str = self.meta['download_date']
            if download_date_str == "":
                warnings.warn("Download date is not speficied in the database. "
                              "Download date used in GTFS." + self.get_weekly_extract_start_date.__name__ +
                              "() defaults to the smallest date when any operations take place.")
                search_start_date = daily_trip_counts['date'].min()
            else:
                search_start_date = datetime.datetime.strptime(download_date_str, "%Y-%m-%d")

        feed_min_date = daily_trip_counts['date'].min()
        feed_max_date = daily_trip_counts['date'].max()
        assert (feed_max_date - feed_min_date >= datetime.timedelta(days=7)), \
            "Dataset is not long enough for providing week long extracts"

        # get first a valid monday where the search for the week can be started:
        next_monday_from_search_start_date = search_start_date + timedelta(days=(7 - search_start_date.weekday()))
        if not (feed_min_date <= next_monday_from_search_start_date <= feed_max_date):
            warnings.warn("The next monday after the (possibly user) specified download date is not present in the database."
                          "Resorting to first monday after the beginning of operations instead.")
            next_monday_from_search_start_date = feed_min_date + timedelta(days=(7 - feed_min_date.weekday()))

        max_trip_count = daily_trip_counts['trip_counts'].quantile(0.95)
        # Take 95th percentile to omit special days, if any exist.

        threshold = weekdays_at_least_of_max * max_trip_count
        threshold_fulfilling_days = daily_trip_counts['trip_counts'] > threshold

        # look forward first
        # get the index of the trip:
        search_start_monday_index = daily_trip_counts[daily_trip_counts['date'] == next_monday_from_search_start_date].index[0]

        # get starting point
        while_loop_monday_index = search_start_monday_index
        while len(daily_trip_counts.index) >= while_loop_monday_index + 7:
            if all(threshold_fulfilling_days[while_loop_monday_index:while_loop_monday_index + 5]):
                row = daily_trip_counts.iloc[while_loop_monday_index]
                if ut:
                    return self.get_day_start_ut(row.date_str)
                else:
                    return row['date']
            while_loop_monday_index += 7

        while_loop_monday_index = search_start_monday_index - 7
        # then backwards
        while while_loop_monday_index >= 0:
            if all(threshold_fulfilling_days[while_loop_monday_index:while_loop_monday_index + 5]):
                row = daily_trip_counts.iloc[while_loop_monday_index]
                if ut:
                    return self.get_day_start_ut(row.date_str)
                else:
                    return row['date']
            while_loop_monday_index -= 7

        raise RuntimeError("No suitable weekly extract start date could be determined!")