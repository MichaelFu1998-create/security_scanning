def prev(self, times=1):
        """Returns a new instance of self
        times is not supported yet.
        """
        return Range(self.start - self.elapse,
                     copy(self.start), tz=self.start.tz)