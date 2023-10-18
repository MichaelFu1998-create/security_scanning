def _avgConnectedSpanForColumn2D(self, columnIndex):
    """
    The range of connectedSynapses per column, averaged for each dimension.
    This value is used to calculate the inhibition radius. This variation of
    the  function only supports a 2 dimensional column topology.

    Parameters:
    ----------------------------
    :param columnIndex:   The index identifying a column in the permanence,
                          potential and connectivity matrices
    """
    assert(self._inputDimensions.size == 2)
    connected = self._connectedSynapses[columnIndex]
    (rows, cols) = connected.reshape(self._inputDimensions).nonzero()
    if  rows.size == 0 and cols.size == 0:
      return 0
    rowSpan = rows.max() - rows.min() + 1
    colSpan = cols.max() - cols.min() + 1
    return numpy.average([rowSpan, colSpan])