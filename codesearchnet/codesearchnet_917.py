def _deleteRecordsFromKNN(self, recordsToDelete):
    """
    This method will remove the given records from the classifier.

    parameters
    ------------
    recordsToDelete - list of records to delete from the classififier
    """
    classifier = self.htm_prediction_model._getAnomalyClassifier()
    knn = classifier.getSelf()._knn

    prototype_idx = classifier.getSelf().getParameter('categoryRecencyList')

    idsToDelete = [r.ROWID for r in recordsToDelete if \
      not r.setByUser and r.ROWID in prototype_idx]

    nProtos = knn._numPatterns
    knn.removeIds(idsToDelete)
    assert knn._numPatterns == nProtos - len(idsToDelete)