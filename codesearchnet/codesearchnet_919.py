def _recomputeRecordFromKNN(self, record):
    """
    return the classified labeling of record
    """
    inputs = {
      "categoryIn": [None],
      "bottomUpIn": self._getStateAnomalyVector(record),
    }

    outputs = {"categoriesOut": numpy.zeros((1,)),
               "bestPrototypeIndices":numpy.zeros((1,)),
               "categoryProbabilitiesOut":numpy.zeros((1,))}

    # Run inference only to capture state before learning
    classifier = self.htm_prediction_model._getAnomalyClassifier()
    knn = classifier.getSelf()._knn

    # Only use points before record to classify and after the wait period.
    classifier_indexes = \
      numpy.array(classifier.getSelf().getParameter('categoryRecencyList'))
    valid_idx = numpy.where(
        (classifier_indexes >= self._autoDetectWaitRecords) &
        (classifier_indexes < record.ROWID)
      )[0].tolist()

    if len(valid_idx) == 0:
      return None

    classifier.setParameter('inferenceMode', True)
    classifier.setParameter('learningMode', False)
    classifier.getSelf().compute(inputs, outputs)
    classifier.setParameter('learningMode', True)

    classifier_distances = classifier.getSelf().getLatestDistances()
    valid_distances = classifier_distances[valid_idx]
    if valid_distances.min() <= self._classificationMaxDist:
      classifier_indexes_prev = classifier_indexes[valid_idx]
      rowID = classifier_indexes_prev[valid_distances.argmin()]
      indexID = numpy.where(classifier_indexes == rowID)[0][0]
      category = classifier.getSelf().getCategoryList()[indexID]
      return category
    return None