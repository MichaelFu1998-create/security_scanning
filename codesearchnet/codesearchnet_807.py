def _bumpUpWeakColumns(self):
    """
    This method increases the permanence values of synapses of columns whose
    activity level has been too low. Such columns are identified by having an
    overlap duty cycle that drops too much below those of their peers. The
    permanence values for such columns are increased.
    """
    weakColumns = numpy.where(self._overlapDutyCycles
                                < self._minOverlapDutyCycles)[0]
    for columnIndex in weakColumns:
      perm = self._permanences[columnIndex].astype(realDType)
      maskPotential = numpy.where(self._potentialPools[columnIndex] > 0)[0]
      perm[maskPotential] += self._synPermBelowStimulusInc
      self._updatePermanencesForColumn(perm, columnIndex, raisePerm=False)