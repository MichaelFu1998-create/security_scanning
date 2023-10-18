def index(self, i, length=None):
        """Return an integer index or None"""
        if self.begin <= i <= self.end:
            index = i - self.BEGIN - self.offset
            if length is None:
                length = self.full_range()
            else:
                length = min(length, self.full_range())

            if 0 <= index < length:
                return index