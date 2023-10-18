def _updateMinDutyCyclesGlobal(self):
    """
    Updates the minimum duty cycles in a global fashion. Sets the minimum duty
    cycles for the overlap all columns to be a percent of the maximum in the
    region, specified by minPctOverlapDutyCycle. Functionality it is equivalent
    to _updateMinDutyCyclesLocal, but this function exploits the globality of
    the computation to perform it in a straightforward, and efficient manner.
    """
    self._minOverlapDutyCycles.fill(
        self._minPctOverlapDutyCycles * self._overlapDutyCycles.max()
      )