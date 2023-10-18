def _calculateOverlap(self, inputVector):
    """
    This function determines each column's overlap with the current input
    vector. The overlap of a column is the number of synapses for that column
    that are connected (permanence value is greater than '_synPermConnected')
    to input bits which are turned on. The implementation takes advantage of
    the SparseBinaryMatrix class to perform this calculation efficiently.

    Parameters:
    ----------------------------
    :param inputVector: a numpy array of 0's and 1's that comprises the input to
                    the spatial pooler.
    """
    overlaps = numpy.zeros(self._numColumns, dtype=realDType)
    self._connectedSynapses.rightVecSumAtNZ_fast(inputVector.astype(realDType),
                                                 overlaps)
    return overlaps