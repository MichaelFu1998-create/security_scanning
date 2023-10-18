def _addRecordToKNN(self, record):
    """
    Adds the record to the KNN classifier.
    """
    knn = self._knnclassifier._knn

    prototype_idx = self._knnclassifier.getParameter('categoryRecencyList')
    category = self._labelListToCategoryNumber(record.anomalyLabel)

    # If record is already in the classifier, overwrite its labeling
    if record.ROWID in prototype_idx:
      knn.prototypeSetCategory(record.ROWID, category)
      return

    # Learn this pattern in the knn
    pattern = self._getStateAnomalyVector(record)
    rowID = record.ROWID
    knn.learn(pattern, category, rowID=rowID)