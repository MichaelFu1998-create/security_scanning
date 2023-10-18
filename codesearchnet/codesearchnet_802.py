def _updateDutyCycles(self, overlaps, activeColumns):
    """
    Updates the duty cycles for each column. The OVERLAP duty cycle is a moving
    average of the number of inputs which overlapped with the each column. The
    ACTIVITY duty cycles is a moving average of the frequency of activation for
    each column.

    Parameters:
    ----------------------------
    :param overlaps:
                    An array containing the overlap score for each column.
                    The overlap score for a column is defined as the number
                    of synapses in a "connected state" (connected synapses)
                    that are connected to input bits which are turned on.
    :param activeColumns:
                    An array containing the indices of the active columns,
                    the sparse set of columns which survived inhibition
    """
    overlapArray = numpy.zeros(self._numColumns, dtype=realDType)
    activeArray = numpy.zeros(self._numColumns, dtype=realDType)
    overlapArray[overlaps > 0] = 1
    activeArray[activeColumns] = 1

    period = self._dutyCyclePeriod
    if (period > self._iterationNum):
      period = self._iterationNum

    self._overlapDutyCycles = self._updateDutyCyclesHelper(
                                self._overlapDutyCycles,
                                overlapArray,
                                period
                              )

    self._activeDutyCycles = self._updateDutyCyclesHelper(
                                self._activeDutyCycles,
                                activeArray,
                                period
                              )