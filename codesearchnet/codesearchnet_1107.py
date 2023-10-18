def getOrphanParticleInfos(self, swarmId, genIdx):
    """Return a list of particleStates for all particles in the given
    swarm generation that have been orphaned.

    Parameters:
    ---------------------------------------------------------------------
    swarmId:  A string representation of the sorted list of encoders in this
                 swarm. For example '__address_encoder.__gym_encoder'

    genIdx:  If not None, only return particles at this specific generation
                  index.

    retval:  (particleStates, modelIds, errScores, completed, matured)
              particleStates: list of particleStates
              modelIds: list of modelIds
              errScores: list of errScores, numpy.inf is plugged in
                              if we don't have a result yet
              completed: list of completed booleans
              matured: list of matured booleans
    """

    entryIdxs = range(len(self._allResults))
    if len(entryIdxs) == 0:
      return ([], [], [], [], [])

    # Get the particles of interest
    particleStates = []
    modelIds = []
    errScores = []
    completedFlags = []
    maturedFlags = []
    for idx in entryIdxs:

      # Get info on this model
      entry = self._allResults[idx]
      if not entry['hidden']:
        continue

      modelParams = entry['modelParams']
      if modelParams['particleState']['swarmId'] != swarmId:
        continue

      isCompleted = entry['completed']
      isMatured = entry['matured']
      particleState = modelParams['particleState']
      particleGenIdx = particleState['genIdx']
      particleId = particleState['id']

      if genIdx is not None and particleGenIdx != genIdx:
        continue

      # Incorporate into return values
      particleStates.append(particleState)
      modelIds.append(entry['modelID'])
      errScores.append(entry['errScore'])
      completedFlags.append(isCompleted)
      maturedFlags.append(isMatured)

    return (particleStates, modelIds, errScores, completedFlags, maturedFlags)