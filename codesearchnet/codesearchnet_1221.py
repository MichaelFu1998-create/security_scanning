def getPosition(self):
    """See comments in base class."""
    position = super(PermuteInt, self).getPosition()
    position =  int(round(position))
    return position