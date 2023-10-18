def setAutoDetectThreshold(self, threshold):
    """
    Sets the autoDetectThreshold.
    TODO: Ensure previously classified points outside of classifier are valid.
    """
    if not (isinstance(threshold, float) or isinstance(threshold, int)):
      raise HTMPredictionModelInvalidArgument("Invalid argument type \'%s\'. threshold "
        "must be a number." % (type(threshold)))

    self._autoDetectThreshold = threshold

    # Update all the states in the classifier's cache
    for state in self.saved_states:
      self._updateState(state)