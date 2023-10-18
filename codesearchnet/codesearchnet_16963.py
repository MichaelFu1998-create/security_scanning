def _format_range_dt(self, d):
        """Format range filter datetime to the closest aggregation interval."""
        if not isinstance(d, six.string_types):
            d = d.isoformat()
        return '{0}||/{1}'.format(
            d, self.dt_rounding_map[self.aggregation_interval])