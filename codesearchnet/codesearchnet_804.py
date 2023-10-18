def _avgColumnsPerInput(self):
    """
    The average number of columns per input, taking into account the topology
    of the inputs and columns. This value is used to calculate the inhibition
    radius. This function supports an arbitrary number of dimensions. If the
    number of column dimensions does not match the number of input dimensions,
    we treat the missing, or phantom dimensions as 'ones'.
    """
    #TODO: extend to support different number of dimensions for inputs and
    # columns
    numDim = max(self._columnDimensions.size, self._inputDimensions.size)
    colDim = numpy.ones(numDim)
    colDim[:self._columnDimensions.size] = self._columnDimensions

    inputDim = numpy.ones(numDim)
    inputDim[:self._inputDimensions.size] = self._inputDimensions

    columnsPerInput = colDim.astype(realDType) / inputDim
    return numpy.average(columnsPerInput)