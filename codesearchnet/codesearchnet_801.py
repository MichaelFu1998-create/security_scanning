def _updateMinDutyCyclesLocal(self):
    """
    Updates the minimum duty cycles. The minimum duty cycles are determined
    locally. Each column's minimum duty cycles are set to be a percent of the
    maximum duty cycles in the column's neighborhood. Unlike
    _updateMinDutyCyclesGlobal, here the values can be quite different for
    different columns.
    """
    for column in xrange(self._numColumns):
      neighborhood = self._getColumnNeighborhood(column)

      maxActiveDuty = self._activeDutyCycles[neighborhood].max()
      maxOverlapDuty = self._overlapDutyCycles[neighborhood].max()

      self._minOverlapDutyCycles[column] = (maxOverlapDuty *
                                            self._minPctOverlapDutyCycles)