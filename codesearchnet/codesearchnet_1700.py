def _chooseCellsToLearnFrom(self, c, i, s, n, activeState):
    """
    Choose n random cells to learn from.

    This function is called several times while learning with timeStep = t-1, so
    we cache the set of candidates for that case. It's also called once with
    timeStep = t, and we cache that set of candidates.

    :returns: tuple (column index, cell index).
    """
    if n <= 0:
      return []

    tmpCandidates = numpy.where(activeState == 1)

    # Candidates can be empty at this point, in which case we return
    # an empty segment list. adaptSegments will do nothing when getting
    # that list.
    if len(tmpCandidates[0]) == 0:
      return []

    if s is None: # new segment
      cands = [syn for syn in zip(tmpCandidates[0], tmpCandidates[1])]
    else:
      # We exclude any synapse that is already in this segment.
      synapsesAlreadyInSegment = set((syn[0], syn[1]) for syn in s.syns)
      cands = [syn for syn in zip(tmpCandidates[0], tmpCandidates[1])
               if (syn[0], syn[1]) not in synapsesAlreadyInSegment]

    # If we have no more candidates than requested, return all of them,
    # no shuffle necessary.
    if len(cands) <= n:
      return cands

    if n == 1: # so that we don't shuffle if only one is needed
      idx = self._random.getUInt32(len(cands))
      return [cands[idx]]  # col and cell idx in col

    # If we need more than one candidate
    indices = numpy.array([j for j in range(len(cands))], dtype='uint32')
    tmp = numpy.zeros(min(n, len(indices)), dtype='uint32')
    self._random.sample(indices, tmp)
    return sorted([cands[j] for j in tmp])