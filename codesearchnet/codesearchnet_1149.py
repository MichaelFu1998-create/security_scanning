def getData(self, n):
    """Returns the next n values for the distribution as a list."""

    records = [self.getNext() for x in range(n)]
    return records