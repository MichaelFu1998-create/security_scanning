def period(self):
        """A Period tuple representing the daily start and end time."""
        start_time = self.root.findtext('daily_start_time')
        if start_time:
            return Period(text_to_time(start_time), text_to_time(self.root.findtext('daily_end_time')))
        return Period(datetime.time(0, 0), datetime.time(23, 59))