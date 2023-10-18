def getTotaln(self):
    """Returns the cumulative n for all the fields in the dataset"""

    n = sum([field.n for field in self.fields])
    return n