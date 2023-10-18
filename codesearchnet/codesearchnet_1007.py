def numSegments(self, cell=None):
    """ 
    Returns the number of segments.

    :param cell: (int) Optional parameter to get the number of segments on a 
           cell.
    :returns: (int) Number of segments on all cells if cell is not specified, or 
              on a specific specified cell
    """
    if cell is not None:
      return len(self._cells[cell]._segments)

    return self._nextFlatIdx - len(self._freeFlatIdxs)