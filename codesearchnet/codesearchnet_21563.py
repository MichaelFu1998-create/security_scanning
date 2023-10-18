def _daily_periods(self, range_start, range_end):
        """Returns an iterator of Period tuples for every day this event is in effect, between range_start
        and range_end."""
        specific = set(self.exceptions.keys())

        return heapq.merge(self.exception_periods(range_start, range_end), *[
            sched.daily_periods(range_start=range_start, range_end=range_end, exclude_dates=specific)
            for sched in self._recurring_schedules
        ])