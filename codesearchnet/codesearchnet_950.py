def finishLearning(self):
    """
    Perform an internal optimization step that speeds up inference if we know
    learning will not be performed anymore. This call may, for example, remove
    all potential inputs to each column.
    """
    if self._tfdr is None:
      raise RuntimeError("Temporal memory has not been initialized")

    if hasattr(self._tfdr, 'finishLearning'):
      self.resetSequenceStates()
      self._tfdr.finishLearning()