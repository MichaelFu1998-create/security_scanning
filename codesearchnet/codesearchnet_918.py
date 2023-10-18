def _deleteRangeFromKNN(self, start=0, end=None):
    """
    This method will remove any stored records within the range from start to
    end. Noninclusive of end.

    parameters
    ------------
    start - integer representing the ROWID of the start of the deletion range,
    end - integer representing the ROWID of the end of the deletion range,
      if None, it will default to end.
    """
    classifier = self.htm_prediction_model._getAnomalyClassifier()
    knn = classifier.getSelf()._knn

    prototype_idx = numpy.array(
      classifier.getSelf().getParameter('categoryRecencyList'))

    if end is None:
      end = prototype_idx.max() + 1

    idsIdxToDelete = numpy.logical_and(prototype_idx >= start,
                                       prototype_idx < end)
    idsToDelete = prototype_idx[idsIdxToDelete]

    nProtos = knn._numPatterns
    knn.removeIds(idsToDelete.tolist())
    assert knn._numPatterns == nProtos - len(idsToDelete)