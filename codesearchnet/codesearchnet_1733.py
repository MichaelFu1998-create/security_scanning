def column_range(self):
        """
        Returns a [*begin*, *end*) tuple describing the range of columns spanned
        by this range. If range spans more than one line, returned *end* is
        the last column of the line.
        """
        if self.begin().line() == self.end().line():
            return self.begin().column(), self.end().column()
        else:
            return self.begin().column(), len(self.begin().source_line()) - 1