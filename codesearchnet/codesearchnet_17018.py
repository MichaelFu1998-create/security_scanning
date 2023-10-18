def extract_date(self, date):
        """Extract date from string if necessary.

        :returns: the extracted date.
        """
        if isinstance(date, six.string_types):
            try:
                date = dateutil.parser.parse(date)
            except ValueError:
                raise ValueError(
                    'Invalid date format for statistic {}.'
                ).format(self.query_name)
        if not isinstance(date, datetime):
            raise TypeError(
                'Invalid date type for statistic {}.'
            ).format(self.query_name)
        return date