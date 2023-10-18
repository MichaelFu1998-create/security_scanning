def getPotential(self, columnIndex, potential):
    """
    :param columnIndex: (int) column index to get potential for.
    :param potential: (list) will be overwritten with column potentials. Must 
           match the number of inputs.
    """
    assert(columnIndex < self._numColumns)
    potential[:] = self._potentialPools[columnIndex]