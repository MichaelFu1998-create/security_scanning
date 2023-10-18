def get_day_start_ut(self, date):
        """
        Get day start time (as specified by GTFS) as unix time in seconds

        Parameters
        ----------
        date : str | unicode | datetime.datetime
            something describing the date

        Returns
        -------
        day_start_ut : int
            start time of the day in unixtime
        """
        if isinstance(date, string_types):
            date = datetime.datetime.strptime(date, '%Y-%m-%d')

        date_noon = datetime.datetime(date.year, date.month, date.day, 12, 0, 0)
        ut_noon = self.unlocalized_datetime_to_ut_seconds(date_noon)
        return ut_noon - 12 * 60 * 60