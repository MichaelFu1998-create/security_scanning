def initStateFrom(self, particleId, particleState, newBest):
    """Init all of our variable positions, velocities, and optionally the best
    result and best position from the given particle.

    If newBest is true, we get the best result and position for this new
    generation from the resultsDB, This is used when evoloving a particle
    because the bestResult and position as stored in was the best AT THE TIME
    THAT PARTICLE STARTED TO RUN and does not include the best since that
    particle completed.
    """
    # Get the update best position and result?
    if newBest:
      (bestResult, bestPosition) = self._resultsDB.getParticleBest(particleId)
    else:
      bestResult = bestPosition = None

    # Replace with the position and velocity of each variable from
    #  saved state
    varStates = particleState['varStates']
    for varName in varStates.keys():
      varState = copy.deepcopy(varStates[varName])
      if newBest:
        varState['bestResult'] = bestResult
      if bestPosition is not None:
        varState['bestPosition'] = bestPosition[varName]
      self.permuteVars[varName].setState(varState)