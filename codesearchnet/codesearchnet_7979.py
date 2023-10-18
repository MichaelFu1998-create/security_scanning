def fetch(self, pivot, session_dates):
        """
        :param pivot: (int) a congressperson document to use as a pivot for scraping the data
        :param session_dates: (list) datetime objects to fetch the start times for
        """

        records = self._all_start_times(pivot, session_dates)
        return pd.DataFrame(records, columns=(
            'date',
            'session',
            'started_at'
        ))