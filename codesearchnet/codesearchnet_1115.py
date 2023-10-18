def _hsStatePeriodicUpdate(self, exhaustedSwarmId=None):
    """
    Periodically, check to see if we should remove a certain field combination
    from evaluation (because it is doing so poorly) or move on to the next
    sprint (add in more fields).

    This method is called from _getCandidateParticleAndSwarm(), which is called
    right before we try and create a new model to run.

    Parameters:
    -----------------------------------------------------------------------
    removeSwarmId:     If not None, force a change to the current set of active
                      swarms by removing this swarm. This is used in situations
                      where we can't find any new unique models to create in
                      this swarm. In these situations, we update the hypersearch
                      state regardless of the timestamp of the last time another
                      worker updated it.

    """
    if self._hsState is None:
      self._hsState =  HsState(self)

    # Read in current state from the DB
    self._hsState.readStateFromDB()

    # This will hold the list of completed swarms that we find
    completedSwarms = set()

    # Mark the exhausted swarm as completing/completed, if any
    if exhaustedSwarmId is not None:
      self.logger.info("Removing swarm %s from the active set "
                       "because we can't find any new unique particle "
                       "positions" % (exhaustedSwarmId))
      # Is it completing or completed?
      (particles, _, _, _, _) = self._resultsDB.getParticleInfos(
                                      swarmId=exhaustedSwarmId, matured=False)
      if len(particles) > 0:
        exhaustedSwarmStatus = 'completing'
      else:
        exhaustedSwarmStatus = 'completed'

    # Kill all swarms that don't need to be explored based on the most recent
    # information.
    if self._killUselessSwarms:
      self._hsState.killUselessSwarms()

    # For all swarms that were in the 'completing' state, see if they have
    # completed yet.
    #
    # Note that we are not quite sure why this doesn't automatically get handled
    # when we receive notification that a model finally completed in a swarm.
    # But, we ARE running into a situation, when speculativeParticles is off,
    # where we have one or more swarms in the 'completing' state even though all
    # models have since finished. This logic will serve as a failsafe against
    # this situation.
    completingSwarms = self._hsState.getCompletingSwarms()
    for swarmId in completingSwarms:
      # Is it completed?
      (particles, _, _, _, _) = self._resultsDB.getParticleInfos(
                                      swarmId=swarmId, matured=False)
      if len(particles) == 0:
        completedSwarms.add(swarmId)

    # Are there any swarms we can remove (because they have matured)?
    completedSwarmGens = self._resultsDB.getMaturedSwarmGenerations()
    priorCompletedSwarms = self._hsState.getCompletedSwarms()
    for (swarmId, genIdx, errScore) in completedSwarmGens:

      # Don't need to report it if the swarm already completed
      if swarmId in priorCompletedSwarms:
        continue

      completedList = self._swarmTerminator.recordDataPoint(
          swarmId=swarmId, generation=genIdx, errScore=errScore)

      # Update status message
      statusMsg = "Completed generation #%d of swarm '%s' with a best" \
                  " errScore of %g" % (genIdx, swarmId, errScore)
      if len(completedList) > 0:
        statusMsg = "%s. Matured swarm(s): %s" % (statusMsg, completedList)
      self.logger.info(statusMsg)
      self._cjDAO.jobSetFields (jobID=self._jobID,
                                fields=dict(engStatus=statusMsg),
                                useConnectionID=False,
                                ignoreUnchanged=True)

      # Special test mode to check which swarms have terminated
      if 'NTA_TEST_recordSwarmTerminations' in os.environ:
        while True:
          resultsStr = self._cjDAO.jobGetFields(self._jobID, ['results'])[0]
          if resultsStr is None:
            results = {}
          else:
            results = json.loads(resultsStr)
          if not 'terminatedSwarms' in results:
            results['terminatedSwarms'] = {}

          for swarm in completedList:
            if swarm not in results['terminatedSwarms']:
              results['terminatedSwarms'][swarm] = (genIdx,
                                    self._swarmTerminator.swarmScores[swarm])

          newResultsStr = json.dumps(results)
          if newResultsStr == resultsStr:
            break
          updated = self._cjDAO.jobSetFieldIfEqual(jobID=self._jobID,
                                                   fieldName='results',
                                                   curValue=resultsStr,
                                                   newValue = json.dumps(results))
          if updated:
            break

      if len(completedList) > 0:
        for name in completedList:
          self.logger.info("Swarm matured: %s. Score at generation %d: "
                           "%s" % (name, genIdx, errScore))
        completedSwarms = completedSwarms.union(completedList)

    if len(completedSwarms)==0 and (exhaustedSwarmId is None):
      return

    # We need to mark one or more swarms as completed, keep trying until
    #  successful, or until some other worker does it for us.
    while True:

      if exhaustedSwarmId is not None:
        self._hsState.setSwarmState(exhaustedSwarmId, exhaustedSwarmStatus)

      # Mark the completed swarms as completed
      for swarmId in completedSwarms:
        self._hsState.setSwarmState(swarmId, 'completed')

      # If nothing changed, we're done
      if not self._hsState.isDirty():
        return

      # Update the shared Hypersearch state now
      # This will do nothing and return False if some other worker beat us to it
      success = self._hsState.writeStateToDB()

      if success:
        # Go through and cancel all models that are still running, except for
        # the best model. Once the best model changes, the one that used to be
        # best (and has  matured) will notice that and stop itself at that point.
        jobResultsStr = self._cjDAO.jobGetFields(self._jobID, ['results'])[0]
        if jobResultsStr is not None:
          jobResults = json.loads(jobResultsStr)
          bestModelId = jobResults.get('bestModel', None)
        else:
          bestModelId = None

        for swarmId in list(completedSwarms):
          (_, modelIds, _, _, _) = self._resultsDB.getParticleInfos(
                                          swarmId=swarmId, completed=False)
          if bestModelId in modelIds:
            modelIds.remove(bestModelId)
          if len(modelIds) == 0:
            continue
          self.logger.info("Killing the following models in swarm '%s' because"
                           "the swarm is being terminated: %s" % (swarmId,
                           str(modelIds)))

          for modelId in modelIds:
            self._cjDAO.modelSetFields(modelId,
                    dict(engStop=ClientJobsDAO.STOP_REASON_KILLED),
                    ignoreUnchanged = True)
        return

      # We were not able to change the state because some other worker beat us
      # to it.
      # Get the new state, and try again to apply our changes.
      self._hsState.readStateFromDB()
      self.logger.debug("New hsState has been set by some other worker to: "
                       " \n%s" % (pprint.pformat(self._hsState._state, indent=4)))