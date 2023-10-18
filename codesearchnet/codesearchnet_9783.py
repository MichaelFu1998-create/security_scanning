def get_suitable_date_for_daily_extract(self, date=None, ut=False):
        """
        Parameters
        ----------
        date : str
        ut : bool
            Whether to return the date as a string or as a an int (seconds after epoch).

        Returns
        -------
        Selects suitable date for daily extract
        Iterates trough the available dates forward and backward from the download date accepting the first day that has
        at least 90 percent of the number of trips of the maximum date. The condition can be changed to something else.
        If the download date is out of range, the process will look through the dates from first to last.
        """
        daily_trips = self.get_trip_counts_per_day()
        max_daily_trips = daily_trips[u'trip_counts'].max(axis=0)
        if date in daily_trips[u'date_str']:
            start_index = daily_trips[daily_trips[u'date_str'] == date].index.tolist()[0]
            daily_trips[u'old_index'] = daily_trips.index
            daily_trips[u'date_dist'] = abs(start_index - daily_trips.index)
            daily_trips = daily_trips.sort_values(by=[u'date_dist', u'old_index']).reindex()
        for row in daily_trips.itertuples():
            if row.trip_counts >= 0.9 * max_daily_trips:
                if ut:
                    return self.get_day_start_ut(row.date_str)
                else:
                    return row.date_str