def clear(self):
    """Clears the state of the KNNClassifier."""
    self._Memory = None
    self._numPatterns = 0
    self._M = None
    self._categoryList = []
    self._partitionIdList = []
    self._partitionIdMap = {}
    self._finishedLearning = False
    self._iterationIdx = -1

    # Fixed capacity KNN
    if self.maxStoredPatterns > 0:
      assert self.useSparseMemory, ("Fixed capacity KNN is implemented only "
                                    "in the sparse memory mode")
      self.fixedCapacity = True
      self._categoryRecencyList = []
    else:
      self.fixedCapacity = False

    # Cached value of the store prototype sizes
    self._protoSizes = None

    # Used by PCA
    self._s = None
    self._vt = None
    self._nc = None
    self._mean = None

    # Used by Network Builder
    self._specificIndexTraining = False
    self._nextTrainingIndices = None