def _finishLearning(self):
    """Does nothing. Kept here for API compatibility """
    if self._doSphering:
      self._finishSphering()

    self._knn.finishLearning()

    # Compute leave-one-out validation accuracy if
    # we actually received non-trivial partition info
    self._accuracy = None