def setSwarmState(self, swarmId, newStatus):
    """Change the given swarm's state to 'newState'. If 'newState' is
    'completed', then bestModelId and bestErrScore must be provided.

    Parameters:
    ---------------------------------------------------------------------
    swarmId:      swarm Id
    newStatus:    new status, either 'active', 'completing', 'completed', or
                    'killed'
    """
    assert (newStatus in ['active', 'completing', 'completed', 'killed'])

    # Set the swarm status
    swarmInfo = self._state['swarms'][swarmId]
    if swarmInfo['status'] == newStatus:
      return

    # If some other worker noticed it as completed, setting it to completing
    #  is obviously old information....
    if swarmInfo['status'] == 'completed' and newStatus == 'completing':
      return

    self._dirty = True
    swarmInfo['status'] = newStatus
    if newStatus == 'completed':
      (modelId, errScore) = self._hsObj._resultsDB.bestModelIdAndErrScore(swarmId)
      swarmInfo['bestModelId'] = modelId
      swarmInfo['bestErrScore'] = errScore

    # If no longer active, remove it from the activeSwarms entry
    if newStatus != 'active' and swarmId in self._state['activeSwarms']:
      self._state['activeSwarms'].remove(swarmId)

    # If new status is 'killed', kill off any running particles in that swarm
    if newStatus=='killed':
      self._hsObj.killSwarmParticles(swarmId)

    # In case speculative particles are enabled, make sure we generate a new
    #  swarm at this time if all of the swarms in the current sprint have
    #  completed. This will insure that we don't mark the sprint as completed
    #  before we've created all the possible swarms.
    sprintIdx = swarmInfo['sprintIdx']
    self.isSprintActive(sprintIdx)

    # Update the sprint status. Check all the swarms that belong to this sprint.
    #  If they are all completed, the sprint is completed.
    sprintInfo = self._state['sprints'][sprintIdx]

    statusCounts = dict(active=0, completing=0, completed=0, killed=0)
    bestModelIds = []
    bestErrScores = []
    for info in self._state['swarms'].itervalues():
      if info['sprintIdx'] != sprintIdx:
        continue
      statusCounts[info['status']] += 1
      if info['status'] == 'completed':
        bestModelIds.append(info['bestModelId'])
        bestErrScores.append(info['bestErrScore'])

    if statusCounts['active'] > 0:
      sprintStatus = 'active'
    elif statusCounts['completing'] > 0:
      sprintStatus = 'completing'
    else:
      sprintStatus = 'completed'
    sprintInfo['status'] = sprintStatus

    # If the sprint is complete, get the best model from all of its swarms and
    #  store that as the sprint best
    if sprintStatus == 'completed':
      if len(bestErrScores) > 0:
        whichIdx = numpy.array(bestErrScores).argmin()
        sprintInfo['bestModelId'] = bestModelIds[whichIdx]
        sprintInfo['bestErrScore'] = bestErrScores[whichIdx]
      else:
        # This sprint was empty, most likely because all particles were
        #  killed. Give it a huge error score
        sprintInfo['bestModelId'] = 0
        sprintInfo['bestErrScore'] = numpy.inf


      # See if our best err score got NO BETTER as compared to a previous
      #  sprint. If so, stop exploring subsequent sprints (lastGoodSprint
      #  is no longer None).
      bestPrior = numpy.inf
      for idx in range(sprintIdx):
        if self._state['sprints'][idx]['status'] == 'completed':
          (_, errScore) = self.bestModelInCompletedSprint(idx)
          if errScore is None:
            errScore = numpy.inf
        else:
          errScore = numpy.inf
        if errScore < bestPrior:
          bestPrior = errScore

      if sprintInfo['bestErrScore'] >= bestPrior:
        self._state['lastGoodSprint'] = sprintIdx-1

      # If ALL sprints up to the last good one are done, the search is now over
      if self._state['lastGoodSprint'] is not None \
            and not self.anyGoodSprintsActive():
        self._state['searchOver'] = True