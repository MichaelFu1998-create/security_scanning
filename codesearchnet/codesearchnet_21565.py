def includes(self, query_date, query_time=None):
        """Does this schedule include the provided time?
        query_date and query_time are date and time objects, interpreted
        in this schedule's timezone"""

        if self.start_date and query_date < self.start_date:
            return False
        if self.end_date and query_date > self.end_date:
            return False
        if query_date.weekday() not in self.weekdays:
            return False

        if not query_time:
            return True

        if query_time >= self.period.start and query_time <= self.period.end:
            return True

        return False