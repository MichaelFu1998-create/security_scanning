def _updateBoostFactorsGlobal(self):
    """
    Update boost factors when global inhibition is used
    """
    # When global inhibition is enabled, the target activation level is
    # the sparsity of the spatial pooler
    if (self._localAreaDensity > 0):
      targetDensity = self._localAreaDensity
    else:
      inhibitionArea = ((2 * self._inhibitionRadius + 1)
                        ** self._columnDimensions.size)
      inhibitionArea = min(self._numColumns, inhibitionArea)
      targetDensity = float(self._numActiveColumnsPerInhArea) / inhibitionArea
      targetDensity = min(targetDensity, 0.5)

    self._boostFactors = numpy.exp(
      (targetDensity - self._activeDutyCycles) * self._boostStrength)