def fetch(self, deputies, start_date, end_date):
        """
        :param deputies: (pandas.DataFrame) a dataframe with deputies data
        :param date_start: (str) date in the format dd/mm/yyyy
        :param date_end: (str) date in the format dd/mm/yyyy
        """
        log.debug("Fetching data for {} deputies from {} -> {}".format(len(deputies), start_date, end_date))

        records = self._all_presences(deputies, start_date, end_date)

        df = pd.DataFrame(records, columns=(
            'term',
            'congressperson_document',
            'congressperson_name',
            'party',
            'state',
            'date',
            'present_on_day',
            'justification',
            'session',
            'presence'
        ))
        return self._translate(df)