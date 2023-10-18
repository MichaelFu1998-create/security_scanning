def setPotential(self, columnIndex, potential):
    """
    Sets the potential mapping for a given column. ``potential`` size must match 
    the number of inputs, and must be greater than ``stimulusThreshold``.
    
    :param columnIndex: (int) column index to set potential for.
    :param potential: (list) value to set.
    """
    assert(columnIndex < self._numColumns)

    potentialSparse = numpy.where(potential > 0)[0]
    if len(potentialSparse) < self._stimulusThreshold:
      raise Exception("This is likely due to a " +
      "value of stimulusThreshold that is too large relative " +
      "to the input size.")

    self._potentialPools.replace(columnIndex, potentialSparse)