def killUselessSwarms(self):
    """See if we can kill off some speculative swarms. If an earlier sprint
    has finally completed, we can now tell which fields should *really* be present
    in the sprints we've already started due to speculation, and kill off the
    swarms that should not have been included.
    """
    # Get number of existing sprints
    numExistingSprints = len(self._state['sprints'])

    # Should we bother killing useless swarms?
    if self._hsObj._searchType == HsSearchType.legacyTemporal:
      if numExistingSprints <= 2:
        return
    else:
      if numExistingSprints <= 1:
        return

    # Form completedSwarms as a list of tuples, each tuple contains:
    #  (swarmName, swarmState, swarmBestErrScore)
    # ex. completedSwarms:
    #    [('a', {...}, 1.4),
    #     ('b', {...}, 2.0),
    #     ('c', {...}, 3.0)]
    completedSwarms = self.getCompletedSwarms()
    completedSwarms = [(swarm, self._state["swarms"][swarm],
                        self._state["swarms"][swarm]["bestErrScore"]) \
                                                for swarm in completedSwarms]

    # Form the completedMatrix. Each row corresponds to a sprint. Each row
    #  contains the list of swarm tuples that belong to that sprint, sorted
    #  by best score. Each swarm tuple contains (swarmName, swarmState,
    #  swarmBestErrScore).
    # ex. completedMatrix:
    #    [(('a', {...}, 1.4), ('b', {...}, 2.0), ('c', {...}, 3.0)),
    #     (('a.b', {...}, 3.0), ('b.c', {...}, 4.0))]
    completedMatrix = [[] for i in range(numExistingSprints)]
    for swarm in completedSwarms:
      completedMatrix[swarm[1]["sprintIdx"]].append(swarm)
    for sprint in completedMatrix:
      sprint.sort(key=itemgetter(2))

    # Form activeSwarms as a list of tuples, each tuple contains:
    #  (swarmName, swarmState, swarmBestErrScore)
    # Include all activeSwarms and completingSwarms
    # ex. activeSwarms:
    #    [('d', {...}, 1.4),
    #     ('e', {...}, 2.0),
    #     ('f', {...}, 3.0)]
    activeSwarms = self.getActiveSwarms()
    # Append the completing swarms
    activeSwarms.extend(self.getCompletingSwarms())
    activeSwarms = [(swarm, self._state["swarms"][swarm],
                     self._state["swarms"][swarm]["bestErrScore"]) \
                                                for swarm in activeSwarms]

    # Form the activeMatrix. Each row corresponds to a sprint. Each row
    #  contains the list of swarm tuples that belong to that sprint, sorted
    #  by best score. Each swarm tuple contains (swarmName, swarmState,
    #  swarmBestErrScore)
    # ex. activeMatrix:
    #    [(('d', {...}, 1.4), ('e', {...}, 2.0), ('f', {...}, 3.0)),
    #     (('d.e', {...}, 3.0), ('e.f', {...}, 4.0))]
    activeMatrix = [[] for i in range(numExistingSprints)]
    for swarm in activeSwarms:
      activeMatrix[swarm[1]["sprintIdx"]].append(swarm)
    for sprint in activeMatrix:
      sprint.sort(key=itemgetter(2))


    # Figure out which active swarms to kill
    toKill = []
    for i in range(1, numExistingSprints):
      for swarm in activeMatrix[i]:
        curSwarmEncoders = swarm[0].split(".")

        # If previous sprint is complete, get the best swarm and kill all active
        #  sprints that are not supersets
        if(len(activeMatrix[i-1])==0):
          # If we are trying all possible 3 field combinations, don't kill any
          #  off in sprint 2
          if i==2 and (self._hsObj._tryAll3FieldCombinations or \
                self._hsObj._tryAll3FieldCombinationsWTimestamps):
            pass
          else:
            bestInPrevious = completedMatrix[i-1][0]
            bestEncoders = bestInPrevious[0].split('.')
            for encoder in bestEncoders:
              if not encoder in curSwarmEncoders:
                toKill.append(swarm)

        # if there are more than two completed encoders sets that are complete and
        # are worse than at least one active swarm in the previous sprint. Remove
        # any combinations that have any pair of them since they cannot have the best encoder.
        #elif(len(completedMatrix[i-1])>1):
        #  for completedSwarm in completedMatrix[i-1]:
        #    activeMatrix[i-1][0][2]<completed

    # Mark the bad swarms as killed
    if len(toKill) > 0:
      print "ParseMe: Killing encoders:" + str(toKill)

    for swarm in toKill:
      self.setSwarmState(swarm[0], "killed")

    return