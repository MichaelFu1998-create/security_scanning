def _getCandidateParticleAndSwarm (self, exhaustedSwarmId=None):
    """Find or create a candidate particle to produce a new model.

    At any one time, there is an active set of swarms in the current sprint, where
    each swarm in the sprint represents a particular combination of fields.
    Ideally, we should try to balance the number of models we have evaluated for
    each swarm at any time.

    This method will see how many models have been evaluated for each active
    swarm in the current active sprint(s) and then try and choose a particle
    from the least represented swarm in the first possible active sprint, with
    the following constraints/rules:

    for each active sprint:
      for each active swarm (preference to those with least# of models so far):
        1.) The particle will be created from new (generation #0) if there are not
        already self._minParticlesPerSwarm particles in the swarm.

        2.) Find the first gen that has a completed particle and evolve that
        particle to the next generation.

        3.) If we got to here, we know that we have satisfied the min# of
        particles for the swarm, and they are all currently running (probably at
        various generation indexes). Go onto the next swarm

      If we couldn't find a swarm to allocate a particle in, go onto the next
      sprint and start allocating particles there....


    Parameters:
    ----------------------------------------------------------------
    exhaustedSwarmId:   If not None, force a change to the current set of active
                        swarms by marking this swarm as either 'completing' or
                        'completed'. If there are still models being evaluaed in
                        it, mark it as 'completing', else 'completed. This is
                        used in situations where we can't find any new unique
                        models to create in this swarm. In these situations, we
                        force an update to the hypersearch state so no other
                        worker wastes time try to use this swarm.

    retval: (exit, particle, swarm)
              exit: If true, this worker is ready to exit (particle and
                      swarm will be None)
              particle: Which particle to run
              swarm: which swarm the particle is in

              NOTE: When particle and swarm are None and exit is False, it
              means that we need to wait for one or more other worker(s) to
              finish their respective models before we can pick a particle
              to run. This will generally only happen when speculativeParticles
              is set to False.
    """
    # Cancel search?
    jobCancel = self._cjDAO.jobGetFields(self._jobID, ['cancel'])[0]
    if jobCancel:
      self._jobCancelled = True
      # Did a worker cancel the job because of an error?
      (workerCmpReason, workerCmpMsg) = self._cjDAO.jobGetFields(self._jobID,
          ['workerCompletionReason', 'workerCompletionMsg'])
      if workerCmpReason == ClientJobsDAO.CMPL_REASON_SUCCESS:
        self.logger.info("Exiting due to job being cancelled")
        self._cjDAO.jobSetFields(self._jobID,
              dict(workerCompletionMsg="Job was cancelled"),
              useConnectionID=False, ignoreUnchanged=True)
      else:
        self.logger.error("Exiting because some worker set the "
              "workerCompletionReason to %s. WorkerCompletionMsg: %s" %
              (workerCmpReason, workerCmpMsg))
      return (True, None, None)

    # Perform periodic updates on the Hypersearch state.
    if self._hsState is not None:
      priorActiveSwarms = self._hsState.getActiveSwarms()
    else:
      priorActiveSwarms = None

    # Update the HypersearchState, checking for matured swarms, and marking
    #  the passed in swarm as exhausted, if any
    self._hsStatePeriodicUpdate(exhaustedSwarmId=exhaustedSwarmId)

    # The above call may have modified self._hsState['activeSwarmIds']
    # Log the current set of active swarms
    activeSwarms = self._hsState.getActiveSwarms()
    if activeSwarms != priorActiveSwarms:
      self.logger.info("Active swarms changed to %s (from %s)" % (activeSwarms,
                                                        priorActiveSwarms))
    self.logger.debug("Active swarms: %s" % (activeSwarms))

    # If too many model errors were detected, exit
    totalCmpModels = self._resultsDB.getNumCompletedModels()
    if totalCmpModels > 5:
      numErrs = self._resultsDB.getNumErrModels()
      if (float(numErrs) / totalCmpModels) > self._maxPctErrModels:
        # Get one of the errors
        errModelIds = self._resultsDB.getErrModelIds()
        resInfo = self._cjDAO.modelsGetResultAndStatus([errModelIds[0]])[0]
        modelErrMsg = resInfo.completionMsg
        cmpMsg = "%s: Exiting due to receiving too many models failing" \
                 " from exceptions (%d out of %d). \nModel Exception: %s" % \
                  (ErrorCodes.tooManyModelErrs, numErrs, totalCmpModels,
                   modelErrMsg)
        self.logger.error(cmpMsg)

        # Cancel the entire job now, if it has not already been cancelled
        workerCmpReason = self._cjDAO.jobGetFields(self._jobID,
            ['workerCompletionReason'])[0]
        if workerCmpReason == ClientJobsDAO.CMPL_REASON_SUCCESS:
          self._cjDAO.jobSetFields(
              self._jobID,
              fields=dict(
                      cancel=True,
                      workerCompletionReason = ClientJobsDAO.CMPL_REASON_ERROR,
                      workerCompletionMsg = cmpMsg),
              useConnectionID=False,
              ignoreUnchanged=True)
        return (True, None, None)

    # If HsState thinks the search is over, exit. It is seeing if the results
    #  on the sprint we just completed are worse than a prior sprint.
    if self._hsState.isSearchOver():
      cmpMsg = "Exiting because results did not improve in most recently" \
                        " completed sprint."
      self.logger.info(cmpMsg)
      self._cjDAO.jobSetFields(self._jobID,
            dict(workerCompletionMsg=cmpMsg),
            useConnectionID=False, ignoreUnchanged=True)
      return (True, None, None)

    # Search successive active sprints, until we can find a candidate particle
    #   to work with
    sprintIdx = -1
    while True:
      # Is this sprint active?
      sprintIdx += 1
      (active, eos) = self._hsState.isSprintActive(sprintIdx)

      # If no more sprints to explore:
      if eos:
        # If any prior ones are still being explored, finish up exploring them
        if self._hsState.anyGoodSprintsActive():
          self.logger.info("No more sprints to explore, waiting for prior"
                         " sprints to complete")
          return (False, None, None)

        # Else, we're done
        else:
          cmpMsg = "Exiting because we've evaluated all possible field " \
                           "combinations"
          self._cjDAO.jobSetFields(self._jobID,
                                   dict(workerCompletionMsg=cmpMsg),
                                   useConnectionID=False, ignoreUnchanged=True)
          self.logger.info(cmpMsg)
          return (True, None, None)

      if not active:
        if not self._speculativeParticles:
          if not self._hsState.isSprintCompleted(sprintIdx):
            self.logger.info("Waiting for all particles in sprint %d to complete"
                          "before evolving any more particles" % (sprintIdx))
            return (False, None, None)
        continue


      # ====================================================================
      # Look for swarms that have particle "holes" in their generations. That is,
      #  an earlier generation with less than minParticlesPerSwarm. This can
      #  happen if a model that was started eariler got orphaned. If we detect
      #  this, start a new particle in that generation.
      swarmIds = self._hsState.getActiveSwarms(sprintIdx)
      for swarmId in swarmIds:
        firstNonFullGenIdx = self._resultsDB.firstNonFullGeneration(
                                swarmId=swarmId,
                                minNumParticles=self._minParticlesPerSwarm)
        if firstNonFullGenIdx is None:
          continue

        if firstNonFullGenIdx < self._resultsDB.highestGeneration(swarmId):
          self.logger.info("Cloning an earlier model in generation %d of swarm "
              "%s (sprintIdx=%s) to replace an orphaned model" % (
                firstNonFullGenIdx, swarmId, sprintIdx))

          # Clone a random orphaned particle from the incomplete generation
          (allParticles, allModelIds, errScores, completed, matured) = \
            self._resultsDB.getOrphanParticleInfos(swarmId, firstNonFullGenIdx)

          if len(allModelIds) > 0:
            # We have seen instances where we get stuck in a loop incessantly
            #  trying to clone earlier models (NUP-1511). My best guess is that
            #  we've already successfully cloned each of the orphaned models at
            #  least once, but still need at least one more. If we don't create
            #  a new particleID, we will never be able to instantiate another
            #  model (since particleID hash is a unique key in the models table).
            #  So, on 1/8/2013 this logic was changed to create a new particleID
            #  whenever we clone an orphan.
            newParticleId = True
            self.logger.info("Cloning an orphaned model")

          # If there is no orphan, clone one of the other particles. We can
          #  have no orphan if this was a speculative generation that only
          #  continued particles completed in the prior generation.
          else:
            newParticleId = True
            self.logger.info("No orphans found, so cloning a non-orphan")
            (allParticles, allModelIds, errScores, completed, matured) = \
            self._resultsDB.getParticleInfos(swarmId=swarmId,
                                             genIdx=firstNonFullGenIdx)

          # Clone that model
          modelId = random.choice(allModelIds)
          self.logger.info("Cloning model %r" % (modelId))
          (particleState, _, _, _, _) = self._resultsDB.getParticleInfo(modelId)
          particle = Particle(hsObj = self,
                              resultsDB = self._resultsDB,
                              flattenedPermuteVars=self._flattenedPermutations,
                              newFromClone=particleState,
                              newParticleId=newParticleId)
          return (False, particle, swarmId)


      # ====================================================================
      # Sort the swarms in priority order, trying the ones with the least
      #  number of models first
      swarmSizes = numpy.array([self._resultsDB.numModels(x) for x in swarmIds])
      swarmSizeAndIdList = zip(swarmSizes, swarmIds)
      swarmSizeAndIdList.sort()
      for (_, swarmId) in swarmSizeAndIdList:

        # -------------------------------------------------------------------
        # 1.) The particle will be created from new (at generation #0) if there
        #   are not already self._minParticlesPerSwarm particles in the swarm.
        (allParticles, allModelIds, errScores, completed, matured) = (
            self._resultsDB.getParticleInfos(swarmId))
        if len(allParticles) < self._minParticlesPerSwarm:
          particle = Particle(hsObj=self,
                              resultsDB=self._resultsDB,
                              flattenedPermuteVars=self._flattenedPermutations,
                              swarmId=swarmId,
                              newFarFrom=allParticles)

          # Jam in the best encoder state found from the first sprint
          bestPriorModel = None
          if sprintIdx >= 1:
            (bestPriorModel, errScore) = self._hsState.bestModelInSprint(0)

          if bestPriorModel is not None:
            self.logger.info("Best model and errScore from previous sprint(%d):"
                              " %s, %g" % (0, str(bestPriorModel), errScore))
            (baseState, modelId, errScore, completed, matured) \
                 = self._resultsDB.getParticleInfo(bestPriorModel)
            particle.copyEncoderStatesFrom(baseState)

            # Copy the best inference type from the earlier sprint
            particle.copyVarStatesFrom(baseState, ['modelParams|inferenceType'])

            # It's best to jiggle the best settings from the prior sprint, so
            #  compute a new position starting from that previous best
            # Only jiggle the vars we copied from the prior model
            whichVars = []
            for varName in baseState['varStates']:
              if ':' in varName:
                whichVars.append(varName)
            particle.newPosition(whichVars)

            self.logger.debug("Particle after incorporating encoder vars from best "
                             "model in previous sprint: \n%s" % (str(particle)))

          return (False, particle, swarmId)

        # -------------------------------------------------------------------
        # 2.) Look for a completed particle to evolve
        # Note that we use lastDescendent. We only want to evolve particles that
        # are at their most recent generation index.
        (readyParticles, readyModelIds, readyErrScores, _, _) = (
            self._resultsDB.getParticleInfos(swarmId, genIdx=None,
                                             matured=True, lastDescendent=True))

        # If we have at least 1 ready particle to evolve...
        if len(readyParticles) > 0:
          readyGenIdxs = [x['genIdx'] for x in readyParticles]
          sortedGenIdxs = sorted(set(readyGenIdxs))
          genIdx = sortedGenIdxs[0]

          # Now, genIdx has the generation of the particle we want to run,
          # Get a particle from that generation and evolve it.
          useParticle = None
          for particle in readyParticles:
            if particle['genIdx'] == genIdx:
              useParticle = particle
              break

          # If speculativeParticles is off, we don't want to evolve a particle
          # into the next generation until all particles in the current
          # generation have completed.
          if not self._speculativeParticles:
            (particles, _, _, _, _) = self._resultsDB.getParticleInfos(
                swarmId, genIdx=genIdx, matured=False)
            if len(particles) > 0:
              continue

          particle = Particle(hsObj=self,
                              resultsDB=self._resultsDB,
                              flattenedPermuteVars=self._flattenedPermutations,
                              evolveFromState=useParticle)
          return (False, particle, swarmId)

        # END: for (swarmSize, swarmId) in swarmSizeAndIdList:
        # No success in this swarm, onto next swarm

      # ====================================================================
      # We couldn't find a particle in this sprint ready to evolve. If
      #  speculative particles is OFF, we have to wait for one or more other
      #  workers to finish up their particles before we can do anything.
      if not self._speculativeParticles:
        self.logger.info("Waiting for one or more of the %s swarms "
            "to complete a generation before evolving any more particles" \
            % (str(swarmIds)))
        return (False, None, None)