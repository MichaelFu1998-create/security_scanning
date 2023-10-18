def next(self, times=1):
        """Returns a new instance of self
        times is not supported yet.
        """
        return Range(copy(self.end),
                     self.end + self.elapse, tz=self.start.tz)