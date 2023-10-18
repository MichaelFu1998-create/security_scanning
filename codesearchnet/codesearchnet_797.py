def getConnectedSynapses(self, columnIndex, connectedSynapses):
    """
    :param connectedSynapses: (list) will be overwritten
    :returns: (iter) the connected synapses for a given column.
              ``connectedSynapses`` size must match the number of inputs"""
    assert(columnIndex < self._numColumns)
    connectedSynapses[:] = self._connectedSynapses[columnIndex]