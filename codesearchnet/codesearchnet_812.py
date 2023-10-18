def _initPermanence(self, potential, connectedPct):
    """
    Initializes the permanences of a column. The method
    returns a 1-D array the size of the input, where each entry in the
    array represents the initial permanence value between the input bit
    at the particular index in the array, and the column represented by
    the 'index' parameter.

    Parameters:
    ----------------------------
    :param potential: A numpy array specifying the potential pool of the column.
                    Permanence values will only be generated for input bits
                    corresponding to indices for which the mask value is 1.
    :param connectedPct: A value between 0 or 1 governing the chance, for each
                         permanence, that the initial permanence value will
                         be a value that is considered connected.
    """
    # Determine which inputs bits will start out as connected
    # to the inputs. Initially a subset of the input bits in a
    # column's potential pool will be connected. This number is
    # given by the parameter "connectedPct"
    perm = numpy.zeros(self._numInputs, dtype=realDType)
    for i in xrange(self._numInputs):
      if (potential[i] < 1):
        continue

      if (self._random.getReal64() <= connectedPct):
        perm[i] = self._initPermConnected()
      else:
        perm[i] = self._initPermNonConnected()

    # Clip off low values. Since we use a sparse representation
    # to store the permanence values this helps reduce memory
    # requirements.
    perm[perm < self._synPermTrimThreshold] = 0

    return perm