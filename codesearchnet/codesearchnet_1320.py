def _initEphemerals(self):
    """
    Initialize attributes that are not saved with the checkpoint.
    """
    self._firstComputeCall = True
    self._accuracy = None
    self._protoScores = None
    self._categoryDistances = None

    self._knn = knn_classifier.KNNClassifier(**self.knnParams)

    for x in ('_partitions', '_useAuxiliary', '_doSphering',
              '_scanInfo', '_protoScores'):
      if not hasattr(self, x):
        setattr(self, x, None)