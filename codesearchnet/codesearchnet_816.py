def _updateBoostFactorsLocal(self):
    """
    Update boost factors when local inhibition is used
    """
    # Determine the target activation level for each column
    # The targetDensity is the average activeDutyCycles of the neighboring
    # columns of each column.
    targetDensity = numpy.zeros(self._numColumns, dtype=realDType)
    for i in xrange(self._numColumns):
      maskNeighbors = self._getColumnNeighborhood(i)
      targetDensity[i] = numpy.mean(self._activeDutyCycles[maskNeighbors])

    self._boostFactors = numpy.exp(
      (targetDensity - self._activeDutyCycles) * self._boostStrength)