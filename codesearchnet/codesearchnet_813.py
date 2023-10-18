def _mapColumn(self, index):
    """
    Maps a column to its respective input index, keeping to the topology of
    the region. It takes the index of the column as an argument and determines
    what is the index of the flattened input vector that is to be the center of
    the column's potential pool. It distributes the columns over the inputs
    uniformly. The return value is an integer representing the index of the
    input bit. Examples of the expected output of this method:
    * If the topology is one dimensional, and the column index is 0, this
      method will return the input index 0. If the column index is 1, and there
      are 3 columns over 7 inputs, this method will return the input index 3.
    * If the topology is two dimensional, with column dimensions [3, 5] and
      input dimensions [7, 11], and the column index is 3, the method
      returns input index 8.

    Parameters:
    ----------------------------
    :param index:   The index identifying a column in the permanence, potential
                    and connectivity matrices.
    :param wrapAround: A boolean value indicating that boundaries should be
                    ignored.
    """
    columnCoords = numpy.unravel_index(index, self._columnDimensions)
    columnCoords = numpy.array(columnCoords, dtype=realDType)
    ratios = columnCoords / self._columnDimensions
    inputCoords = self._inputDimensions * ratios
    inputCoords += 0.5 * self._inputDimensions / self._columnDimensions
    inputCoords = inputCoords.astype(int)
    inputIndex = numpy.ravel_multi_index(inputCoords, self._inputDimensions)
    return inputIndex