def update(self, modelID, modelParams, modelParamsHash, metricResult,
             completed, completionReason, matured, numRecords):
    """ Insert a new entry or update an existing one. If this is an update
    of an existing entry, then modelParams will be None

    Parameters:
    --------------------------------------------------------------------
    modelID:       globally unique modelID of this model
    modelParams:    params dict for this model, or None if this is just an update
                    of a model that it already previously reported on.

                    See the comments for the createModels() method for
                    a description of this dict.

    modelParamsHash:  hash of the modelParams dict, generated by the worker
                    that put it into the model database.
    metricResult:   value on the optimizeMetric for this model.
                    May be None if we have no results yet.
    completed:      True if the model has completed evaluation, False if it
                      is still running (and these are online results)
    completionReason: One of the ClientJobsDAO.CMPL_REASON_XXX equates
    matured:        True if this model has matured
    numRecords:     Number of records that have been processed so far by this
                      model.

    retval: Canonicalized result on the optimize metric
    """
    # The modelParamsHash must always be provided - it can change after a
    #  model is inserted into the models table if it got detected as an
    #  orphan
    assert (modelParamsHash is not None)

    # We consider a model metricResult as "final" if it has completed or
    #  matured. By default, assume anything that has completed has matured
    if completed:
      matured = True

    # Get the canonicalized optimize metric results. For this metric, lower
    #  is always better
    if metricResult is not None and matured and \
                       completionReason in [ClientJobsDAO.CMPL_REASON_EOF,
                                            ClientJobsDAO.CMPL_REASON_STOPPED]:
      # Canonicalize the error score so that lower is better
      if self._hsObj._maximize:
        errScore = -1 * metricResult
      else:
        errScore = metricResult

      if errScore < self._bestResult:
        self._bestResult = errScore
        self._bestModelID = modelID
        self._hsObj.logger.info("New best model after %d evaluations: errScore "
              "%g on model %s" % (len(self._allResults), self._bestResult,
                                  self._bestModelID))

    else:
      errScore = numpy.inf

    # If this model completed with an unacceptable completion reason, set the
    #  errScore to infinite and essentially make this model invisible to
    #  further queries
    if completed and completionReason in [ClientJobsDAO.CMPL_REASON_ORPHAN]:
      errScore = numpy.inf
      hidden = True
    else:
      hidden = False

    # Update our set of erred models and completed models. These are used
    #  to determine if we should abort the search because of too many errors
    if completed:
      self._completedModels.add(modelID)
      self._numCompletedModels = len(self._completedModels)
      if completionReason == ClientJobsDAO.CMPL_REASON_ERROR:
        self._errModels.add(modelID)
        self._numErrModels = len(self._errModels)

    # Are we creating a new entry?
    wasHidden = False
    if modelID not in self._modelIDToIdx:
      assert (modelParams is not None)
      entry = dict(modelID=modelID, modelParams=modelParams,
                   modelParamsHash=modelParamsHash,
                   errScore=errScore, completed=completed,
                   matured=matured, numRecords=numRecords, hidden=hidden)
      self._allResults.append(entry)
      entryIdx = len(self._allResults) - 1
      self._modelIDToIdx[modelID] = entryIdx

      self._paramsHashToIndexes[modelParamsHash] = entryIdx

      swarmId = modelParams['particleState']['swarmId']
      if not hidden:
        # Update the list of particles in each swarm
        if swarmId in self._swarmIdToIndexes:
          self._swarmIdToIndexes[swarmId].append(entryIdx)
        else:
          self._swarmIdToIndexes[swarmId] = [entryIdx]

        # Update number of particles at each generation in this swarm
        genIdx = modelParams['particleState']['genIdx']
        numPsEntry = self._swarmNumParticlesPerGeneration.get(swarmId, [0])
        while genIdx >= len(numPsEntry):
          numPsEntry.append(0)
        numPsEntry[genIdx] += 1
        self._swarmNumParticlesPerGeneration[swarmId] = numPsEntry

    # Replacing an existing one
    else:
      entryIdx = self._modelIDToIdx.get(modelID, None)
      assert (entryIdx is not None)
      entry = self._allResults[entryIdx]
      wasHidden = entry['hidden']

      # If the paramsHash changed, note that. This can happen for orphaned
      #  models
      if entry['modelParamsHash'] != modelParamsHash:

        self._paramsHashToIndexes.pop(entry['modelParamsHash'])
        self._paramsHashToIndexes[modelParamsHash] = entryIdx
        entry['modelParamsHash'] = modelParamsHash

      # Get the model params, swarmId, and genIdx
      modelParams = entry['modelParams']
      swarmId = modelParams['particleState']['swarmId']
      genIdx = modelParams['particleState']['genIdx']

      # If this particle just became hidden, remove it from our swarm counts
      if hidden and not wasHidden:
        assert (entryIdx in self._swarmIdToIndexes[swarmId])
        self._swarmIdToIndexes[swarmId].remove(entryIdx)
        self._swarmNumParticlesPerGeneration[swarmId][genIdx] -= 1

      # Update the entry for the latest info
      entry['errScore']  = errScore
      entry['completed'] = completed
      entry['matured'] = matured
      entry['numRecords'] = numRecords
      entry['hidden'] = hidden

    # Update the particle best errScore
    particleId = modelParams['particleState']['id']
    genIdx = modelParams['particleState']['genIdx']
    if matured and not hidden:
      (oldResult, pos) = self._particleBest.get(particleId, (numpy.inf, None))
      if errScore < oldResult:
        pos = Particle.getPositionFromState(modelParams['particleState'])
        self._particleBest[particleId] = (errScore, pos)

    # Update the particle latest generation index
    prevGenIdx = self._particleLatestGenIdx.get(particleId, -1)
    if not hidden and genIdx > prevGenIdx:
      self._particleLatestGenIdx[particleId] = genIdx
    elif hidden and not wasHidden and genIdx == prevGenIdx:
      self._particleLatestGenIdx[particleId] = genIdx-1

    # Update the swarm best score
    if not hidden:
      swarmId = modelParams['particleState']['swarmId']
      if not swarmId in self._swarmBestOverall:
        self._swarmBestOverall[swarmId] = []

      bestScores = self._swarmBestOverall[swarmId]
      while genIdx >= len(bestScores):
        bestScores.append((None, numpy.inf))
      if errScore < bestScores[genIdx][1]:
        bestScores[genIdx] = (modelID, errScore)

    # Update the self._modifiedSwarmGens flags to support the
    #   getMaturedSwarmGenerations() call.
    if not hidden:
      key = (swarmId, genIdx)
      if not key in self._maturedSwarmGens:
        self._modifiedSwarmGens.add(key)

    return errScore