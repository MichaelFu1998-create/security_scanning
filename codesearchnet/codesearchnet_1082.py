def getTotalw(self):
    """Returns the cumulative w for all the fields in the dataset"""

    w = sum([field.w for field in self.fields])
    return w