def bestModelIdAndErrScore(self, swarmId=None, genIdx=None):
    """Return the model ID of the model with the best result so far and
    it's score on the optimize metric. If swarm is None, then it returns
    the global best, otherwise it returns the best for the given swarm
    for all generatons up to and including genIdx.

    Parameters:
    ---------------------------------------------------------------------
    swarmId:  A string representation of the sorted list of encoders in this
                 swarm. For example '__address_encoder.__gym_encoder'
    genIdx:   consider the best in all generations up to and including this
                generation if not None.
    retval:  (modelID, result)
    """
    if swarmId is None:
      return (self._bestModelID, self._bestResult)

    else:
      if swarmId not in self._swarmBestOverall:
        return (None, numpy.inf)


      # Get the best score, considering the appropriate generations
      genScores = self._swarmBestOverall[swarmId]
      bestModelId = None
      bestScore = numpy.inf

      for (i, (modelId, errScore)) in enumerate(genScores):
        if genIdx is not None and i > genIdx:
          break
        if errScore < bestScore:
          bestScore = errScore
          bestModelId = modelId

      return (bestModelId, bestScore)