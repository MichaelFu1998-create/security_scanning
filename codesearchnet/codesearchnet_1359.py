def _getShiftedGroundTruth(self, groundTruth):
    """ Utility function that saves the passed in groundTruth into a local
    history buffer, and returns the groundTruth from self._predictionSteps ago,
    where self._predictionSteps is defined by the 'steps' parameter.
    This can be called from the beginning of a derived class's addInstance()
    before it passes groundTruth and prediction onto accumulate().
    """

    # Save this ground truth into our input history
    self._groundTruthHistory.append(groundTruth)

    # This is only supported when _predictionSteps has one item in it
    assert (len(self._predictionSteps) == 1)
    # Return the one from N steps ago
    if len(self._groundTruthHistory) > self._predictionSteps[0]:
      return self._groundTruthHistory.popleft()
    else:
      if hasattr(groundTruth, '__iter__'):
        return [None] * len(groundTruth)
      else:
        return None