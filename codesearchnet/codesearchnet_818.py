def _inhibitColumns(self, overlaps):
    """
    Performs inhibition. This method calculates the necessary values needed to
    actually perform inhibition and then delegates the task of picking the
    active columns to helper functions.

    Parameters:
    ----------------------------
    :param overlaps: an array containing the overlap score for each  column.
                    The overlap score for a column is defined as the number
                    of synapses in a "connected state" (connected synapses)
                    that are connected to input bits which are turned on.
    """
    # determine how many columns should be selected in the inhibition phase.
    # This can be specified by either setting the 'numActiveColumnsPerInhArea'
    # parameter or the 'localAreaDensity' parameter when initializing the class
    if (self._localAreaDensity > 0):
      density = self._localAreaDensity
    else:
      inhibitionArea = ((2*self._inhibitionRadius + 1)
                                    ** self._columnDimensions.size)
      inhibitionArea = min(self._numColumns, inhibitionArea)
      density = float(self._numActiveColumnsPerInhArea) / inhibitionArea
      density = min(density, 0.5)

    if self._globalInhibition or \
      self._inhibitionRadius > max(self._columnDimensions):
      return self._inhibitColumnsGlobal(overlaps, density)
    else:
      return self._inhibitColumnsLocal(overlaps, density)