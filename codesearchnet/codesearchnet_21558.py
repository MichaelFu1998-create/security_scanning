def next_interval(self, after=None):
        """Returns the next Period this event is in effect, or None if the event
        has no remaining periods."""
        if after is None:
            after = timezone.now()
        after = self.to_timezone(after)
        return next(self.intervals(range_start=after), None)