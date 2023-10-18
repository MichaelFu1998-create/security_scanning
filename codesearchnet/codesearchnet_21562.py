def includes(self, query):
        """Does this schedule include the provided time?
        query should be a datetime (naive or timezone-aware)"""
        query = self.to_timezone(query)
        query_date = query.date()
        query_time = query.time()

        # Is the provided time an exception for this schedule?
        specific = self.exceptions.get(query_date)
        if specific is not None:
            if len(specific) == 0:
                # Not in effect on this day
                return False
            for period in specific:
                if query_time >= period.start and query_time <= period.end:
                    return True
            return False

        # It's not an exception. Is it within a recurring schedule?
        return any(sched.includes(query_date, query_time) for sched in self._recurring_schedules)