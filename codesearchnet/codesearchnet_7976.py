def fetch(self, start_date, end_date):
        """
        Fetches official missions within the given date range
        """

        records = []
        for two_months_range in self._generate_ranges(start_date, end_date):
            log.debug(two_months_range)
            for record in self._fetch_missions_for_range(two_months_range[0], two_months_range[1]):
                records.append(record)

        df = pd.DataFrame(records, columns=[
            'participant',
            'destination',
            'subject',
            'start',
            'end',
            'canceled',
            'report_status',
            'report_details_link'
        ])

        translate_column(df, 'report_status', {
            'Disponível': 'Available',
            'Pendente': 'Pending',
            'Em análise': 'Analysing',
            'Não se aplica': 'Does not apply'
        })
        translate_column(df, 'canceled', {
            'Não': 'No',
            'Sim': 'Yes'
        })

        return df.drop_duplicates()