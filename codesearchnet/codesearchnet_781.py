def _recomputeRecordFromKNN(self, record):
    """
    returns the classified labeling of record
    """
    inputs = {
      "categoryIn": [None],
      "bottomUpIn": self._getStateAnomalyVector(record),
    }

    outputs = {"categoriesOut": numpy.zeros((1,)),
               "bestPrototypeIndices":numpy.zeros((1,)),
               "categoryProbabilitiesOut":numpy.zeros((1,))}

    # Only use points before record to classify and after the wait period.
    classifier_indexes = numpy.array(
        self._knnclassifier.getParameter('categoryRecencyList'))
    valid_idx = numpy.where(
        (classifier_indexes >= self.getParameter('trainRecords')) &
        (classifier_indexes < record.ROWID)
      )[0].tolist()

    if len(valid_idx) == 0:
      return None

    self._knnclassifier.setParameter('inferenceMode', None, True)
    self._knnclassifier.setParameter('learningMode', None, False)
    self._knnclassifier.compute(inputs, outputs)
    self._knnclassifier.setParameter('learningMode', None, True)

    classifier_distances = self._knnclassifier.getLatestDistances()
    valid_distances = classifier_distances[valid_idx]
    if valid_distances.min() <= self._classificationMaxDist:
      classifier_indexes_prev = classifier_indexes[valid_idx]
      rowID = classifier_indexes_prev[valid_distances.argmin()]
      indexID = numpy.where(classifier_indexes == rowID)[0][0]
      category = self._knnclassifier.getCategoryList()[indexID]
      return category
    return None