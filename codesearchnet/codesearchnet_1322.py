def setParameter(self, name, index, value):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.setParameter`.
    """
    if name == "learningMode":
      self.learningMode = bool(int(value))
      self._epoch = 0
    elif name == "inferenceMode":
      self._epoch = 0
      if int(value) and not self.inferenceMode:
        self._finishLearning()
      self.inferenceMode = bool(int(value))
    elif name == "distanceNorm":
      self._knn.distanceNorm = value
    elif name == "distanceMethod":
      self._knn.distanceMethod = value
    elif name == "keepAllDistances":
      self.keepAllDistances = bool(value)
      if not self.keepAllDistances:
        # Discard all distances except the latest
        if self._protoScores is not None and self._protoScores.shape[0] > 1:
          self._protoScores = self._protoScores[-1,:]
        if self._protoScores is not None:
          self._protoScoreCount = 1
        else:
          self._protoScoreCount = 0
    elif name == "verbosity":
      self.verbosity = value
      self._knn.verbosity = value
    else:
      return PyRegion.setParameter(self, name, index, value)