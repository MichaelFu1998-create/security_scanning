def get_trip_counts_per_day(self):
        """
        Get trip counts per day between the start and end day of the feed.

        Returns
        -------
        trip_counts : pandas.DataFrame
            Has columns "date_str" (dtype str) "trip_counts" (dtype int)
        """
        query = "SELECT date, count(*) AS number_of_trips FROM day_trips GROUP BY date"
        # this yields the actual data
        trip_counts_per_day = pd.read_sql_query(query, self.conn, index_col="date")
        # the rest is simply code for filling out "gaps" in the time span
        # (necessary for some visualizations)
        max_day = trip_counts_per_day.index.max()
        min_day = trip_counts_per_day.index.min()
        min_date = datetime.datetime.strptime(min_day, '%Y-%m-%d')
        max_date = datetime.datetime.strptime(max_day, '%Y-%m-%d')
        num_days = (max_date - min_date).days
        dates = [min_date + datetime.timedelta(days=x) for x in range(num_days + 1)]
        trip_counts = []
        date_strings = []
        for date in dates:
            date_string = date.strftime("%Y-%m-%d")
            date_strings.append(date_string)
            try:
                value = trip_counts_per_day.loc[date_string, 'number_of_trips']
            except KeyError:
                # set value to 0 if dsut is not present, i.e. when no trips
                # take place on that day
                value = 0
            trip_counts.append(value)
        # check that all date_strings are included (move this to tests?)
        for date_string in trip_counts_per_day.index:
            assert date_string in date_strings
        data = {"date": dates, "date_str": date_strings, "trip_counts": trip_counts}
        return pd.DataFrame(data)