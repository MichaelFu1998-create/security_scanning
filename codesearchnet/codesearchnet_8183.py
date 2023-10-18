def next(self, length):
        """Return a new segment starting right after self in the same buffer."""
        return Segment(self.strip, length, self.offset + self.length)