def bestModelInSprint(self, sprintIdx):
    """Return the best model ID and it's errScore from the given sprint,
    which may still be in progress. This returns the best score from all models
    in the sprint which have matured so far.

    Parameters:
    ---------------------------------------------------------------------
    retval:   (modelId, errScore)
    """
    # Get all the swarms in this sprint
    swarms = self.getAllSwarms(sprintIdx)

    # Get the best model and score from each swarm
    bestModelId = None
    bestErrScore = numpy.inf
    for swarmId in swarms:
      (modelId, errScore) = self._hsObj._resultsDB.bestModelIdAndErrScore(swarmId)
      if errScore < bestErrScore:
        bestModelId = modelId
        bestErrScore = errScore

    return (bestModelId, bestErrScore)