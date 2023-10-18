def _deleteRangeFromKNN(self, start=0, end=None):
    """
    Removes any stored records within the range from start to
    end. Noninclusive of end.

    parameters
    ------------
    start - integer representing the ROWID of the start of the deletion range,
    end - integer representing the ROWID of the end of the deletion range,
      if None, it will default to end.
    """
    prototype_idx = numpy.array(
      self._knnclassifier.getParameter('categoryRecencyList'))

    if end is None:
      end = prototype_idx.max() + 1

    idsIdxToDelete = numpy.logical_and(prototype_idx >= start,
                                       prototype_idx < end)
    idsToDelete = prototype_idx[idsIdxToDelete]

    nProtos = self._knnclassifier._knn._numPatterns
    self._knnclassifier._knn.removeIds(idsToDelete.tolist())
    assert self._knnclassifier._knn._numPatterns == nProtos - len(idsToDelete)