def getPredictiveCells(self):
    """ Returns the indices of the predictive cells.

    :returns: (list) Indices of predictive cells.
    """
    previousCell = None
    predictiveCells = []
    for segment in self.activeSegments:
      if segment.cell != previousCell:
        predictiveCells.append(segment.cell)
        previousCell = segment.cell

    return predictiveCells