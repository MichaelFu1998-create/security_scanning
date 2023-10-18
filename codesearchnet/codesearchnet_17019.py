def validate_arguments(self, interval, start_date, end_date, **kwargs):
        """Validate query arguments."""
        if interval not in self.allowed_intervals:
            raise InvalidRequestInputError(
                'Invalid aggregation time interval for statistic {}.'
            ).format(self.query_name)
        if set(kwargs) < set(self.required_filters):
            raise InvalidRequestInputError(
                'Missing one of the required parameters {0} in '
                'query {1}'.format(set(self.required_filters.keys()),
                                   self.query_name)
            )