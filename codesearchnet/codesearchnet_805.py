def _avgConnectedSpanForColumn1D(self, columnIndex):
    """
    The range of connected synapses for column. This is used to
    calculate the inhibition radius. This variation of the function only
    supports a 1 dimensional column topology.

    Parameters:
    ----------------------------
    :param columnIndex:   The index identifying a column in the permanence,
                          potential and connectivity matrices
    """
    assert(self._inputDimensions.size == 1)
    connected = self._connectedSynapses[columnIndex].nonzero()[0]
    if connected.size == 0:
      return 0
    else:
      return max(connected) - min(connected) + 1