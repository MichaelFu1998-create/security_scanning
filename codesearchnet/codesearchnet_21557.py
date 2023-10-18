def intervals(self, range_start=datetime.datetime.min, range_end=datetime.datetime.max):
        """Returns a list of tuples of start/end datetimes for when the schedule
        is active during the provided range."""
        raise NotImplementedError