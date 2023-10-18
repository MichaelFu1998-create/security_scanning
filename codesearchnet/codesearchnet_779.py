def _deleteRecordsFromKNN(self, recordsToDelete):
    """
    Removes the given records from the classifier.

    parameters
    ------------
    recordsToDelete - list of records to delete from the classififier
    """
    prototype_idx = self._knnclassifier.getParameter('categoryRecencyList')

    idsToDelete = ([r.ROWID for r in recordsToDelete if
      not r.setByUser and r.ROWID in prototype_idx])

    nProtos = self._knnclassifier._knn._numPatterns
    self._knnclassifier._knn.removeIds(idsToDelete)
    assert self._knnclassifier._knn._numPatterns == nProtos - len(idsToDelete)