def _updatePermanencesForColumn(self, perm, columnIndex, raisePerm=True):
    """
    This method updates the permanence matrix with a column's new permanence
    values. The column is identified by its index, which reflects the row in
    the matrix, and the permanence is given in 'dense' form, i.e. a full
    array containing all the zeros as well as the non-zero values. It is in
    charge of implementing 'clipping' - ensuring that the permanence values are
    always between 0 and 1 - and 'trimming' - enforcing sparsity by zeroing out
    all permanence values below '_synPermTrimThreshold'. It also maintains
    the consistency between 'self._permanences' (the matrix storing the
    permanence values), 'self._connectedSynapses', (the matrix storing the bits
    each column is connected to), and 'self._connectedCounts' (an array storing
    the number of input bits each column is connected to). Every method wishing
    to modify the permanence matrix should do so through this method.

    Parameters:
    ----------------------------
    :param perm:    An array of permanence values for a column. The array is
                    "dense", i.e. it contains an entry for each input bit, even
                    if the permanence value is 0.
    :param index:   The index identifying a column in the permanence, potential
                    and connectivity matrices
    :param raisePerm: A boolean value indicating whether the permanence values
                    should be raised until a minimum number are synapses are in
                    a connected state. Should be set to 'false' when a direct
                    assignment is required.
    """
    maskPotential = numpy.where(self._potentialPools[columnIndex] > 0)[0]
    if raisePerm:
      self._raisePermanenceToThreshold(perm, maskPotential)
    perm[perm < self._synPermTrimThreshold] = 0
    numpy.clip(perm, self._synPermMin, self._synPermMax, out=perm)
    newConnected = numpy.where(perm >=
                               self._synPermConnected - PERMANENCE_EPSILON)[0]
    self._permanences.update(columnIndex, perm)
    self._connectedSynapses.replace(columnIndex, newConnected)
    self._connectedCounts[columnIndex] = newConnected.size