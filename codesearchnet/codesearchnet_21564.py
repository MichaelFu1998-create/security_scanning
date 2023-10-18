def intervals(self, range_start=datetime.datetime.min, range_end=datetime.datetime.max):
        """Returns an iterator of Period tuples for continuous stretches of time during
        which this event is in effect, between range_start and range_end."""

        # At the moment the algorithm works on periods split by calendar day, one at a time,
        # merging them if they're continuous; to avoid looping infinitely for infinitely long
        # periods, it splits periods as soon as they reach 60 days.
        # This algorithm could likely be improved to get rid of this restriction and improve
        # efficiency, so code should not rely on this behaviour.

        current_period = None
        max_continuous_days = 60

        range_start = self.to_timezone(range_start)
        range_end = self.to_timezone(range_end)

        for period in self._daily_periods(range_start.date(), range_end.date()):
            if period.end < range_start or period.start > range_end:
                continue
            if current_period is None:
                current_period = period
            else:
                if ( ((period.start < current_period.end)
                        or (period.start - current_period.end) <= datetime.timedelta(minutes=1))
                        and (current_period.end - current_period.start) < datetime.timedelta(days=max_continuous_days)):
                    # Merge
                    current_period = Period(current_period.start, period.end)
                else:
                    yield current_period
                    current_period = period
        if current_period:
            yield current_period