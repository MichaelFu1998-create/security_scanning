def gaps(self, min_length = 1):
        '''Finds the positions of all gaps in the sequence that are at least min_length long. Returns a list of Intervals. Coords are zero-based'''
        gaps = []
        regex = re.compile('N+', re.IGNORECASE)
        for m in regex.finditer(self.seq):
             if m.span()[1] - m.span()[0] + 1 >= min_length:
                 gaps.append(intervals.Interval(m.span()[0], m.span()[1] - 1))
        return gaps