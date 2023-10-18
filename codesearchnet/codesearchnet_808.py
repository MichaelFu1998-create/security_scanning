def _raisePermanenceToThreshold(self, perm, mask):
    """
    This method ensures that each column has enough connections to input bits
    to allow it to become active. Since a column must have at least
    'self._stimulusThreshold' overlaps in order to be considered during the
    inhibition phase, columns without such minimal number of connections, even
    if all the input bits they are connected to turn on, have no chance of
    obtaining the minimum threshold. For such columns, the permanence values
    are increased until the minimum number of connections are formed.


    Parameters:
    ----------------------------
    :param perm:    An array of permanence values for a column. The array is
                    "dense", i.e. it contains an entry for each input bit, even
                    if the permanence value is 0.
    :param mask:    the indices of the columns whose permanences need to be
                    raised.
    """
    if len(mask) < self._stimulusThreshold:
      raise Exception("This is likely due to a " +
      "value of stimulusThreshold that is too large relative " +
      "to the input size. [len(mask) < self._stimulusThreshold]")

    numpy.clip(perm, self._synPermMin, self._synPermMax, out=perm)
    while True:
      numConnected = numpy.nonzero(
        perm > self._synPermConnected - PERMANENCE_EPSILON)[0].size

      if numConnected >= self._stimulusThreshold:
        return
      perm[mask] += self._synPermBelowStimulusInc