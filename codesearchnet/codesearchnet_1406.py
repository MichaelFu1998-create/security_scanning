def _getDistances(self, inputPattern, partitionId=None):
    """Return the distances from inputPattern to all stored patterns.

    :param inputPattern The pattern from which distances to all other patterns
        are returned

    :param partitionId If provided, ignore all training vectors with this
        partitionId.
    """
    if not self._finishedLearning:
      self.finishLearning()
      self._finishedLearning = True

    if self._vt is not None and len(self._vt) > 0:
      inputPattern = numpy.dot(self._vt, inputPattern - self._mean)

    sparseInput = self._sparsifyVector(inputPattern)

    # Compute distances
    dist = self._calcDistance(sparseInput)
    # Invalidate results where category is -1
    if self._specificIndexTraining:
      dist[numpy.array(self._categoryList) == -1] = numpy.inf

    # Ignore vectors with this partition id by setting their distances to inf
    if partitionId is not None:
      dist[self._partitionIdMap.get(partitionId, [])] = numpy.inf

    return dist