def getParticleInfos(self, swarmId=None, genIdx=None, completed=None,
                       matured=None, lastDescendent=False):
    """Return a list of particleStates for all particles we know about in
    the given swarm, their model Ids, and metric results.

    Parameters:
    ---------------------------------------------------------------------
    swarmId:  A string representation of the sorted list of encoders in this
                 swarm. For example '__address_encoder.__gym_encoder'

    genIdx:  If not None, only return particles at this specific generation
                  index.

    completed:   If not None, only return particles of the given state (either
                completed if 'completed' is True, or running if 'completed'
                is false

    matured:   If not None, only return particles of the given state (either
                matured if 'matured' is True, or not matured if 'matured'
                is false. Note that any model which has completed is also
                considered matured.

    lastDescendent: If True, only return particles that are the last descendent,
                that is, the highest generation index for a given particle Id

    retval:  (particleStates, modelIds, errScores, completed, matured)
              particleStates: list of particleStates
              modelIds: list of modelIds
              errScores: list of errScores, numpy.inf is plugged in
                              if we don't have a result yet
              completed: list of completed booleans
              matured: list of matured booleans
    """
    # The indexes of all the models in this swarm. This list excludes hidden
    #  (orphaned) models.
    if swarmId is not None:
      entryIdxs = self._swarmIdToIndexes.get(swarmId, [])
    else:
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
      entry = self._allResults[idx]

      # If this entry is hidden (i.e. it was an orphaned model), it should
      #  not be in this list
      if swarmId is not None:
        assert (not entry['hidden'])

      # Get info on this model
      modelParams = entry['modelParams']
      isCompleted = entry['completed']
      isMatured = entry['matured']
      particleState = modelParams['particleState']
      particleGenIdx = particleState['genIdx']
      particleId = particleState['id']

      if genIdx is not None and particleGenIdx != genIdx:
        continue

      if completed is not None and (completed != isCompleted):
        continue

      if matured is not None and (matured != isMatured):
        continue

      if lastDescendent \
              and (self._particleLatestGenIdx[particleId] != particleGenIdx):
        continue

      # Incorporate into return values
      particleStates.append(particleState)
      modelIds.append(entry['modelID'])
      errScores.append(entry['errScore'])
      completedFlags.append(isCompleted)
      maturedFlags.append(isMatured)


    return (particleStates, modelIds, errScores, completedFlags, maturedFlags)