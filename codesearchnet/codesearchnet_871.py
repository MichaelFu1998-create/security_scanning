def isSprintActive(self, sprintIdx):
    """If the given sprint exists and is active, return active=True.

    If the sprint does not exist yet, this call will create it (and return
    active=True). If it already exists, but is completing or complete, return
    active=False.

    If sprintIdx is past the end of the possible sprints, return
      active=False, noMoreSprints=True

    IMPORTANT: When speculative particles are enabled, this call has some
    special processing to handle speculative sprints:

      * When creating a new speculative sprint (creating sprint N before
      sprint N-1 has completed), it initially only puts in only ONE swarm into
      the sprint.

      * Every time it is asked if sprint N is active, it also checks to see if
      it is time to add another swarm to the sprint, and adds a new swarm if
      appropriate before returning active=True

      * We decide it is time to add a new swarm to a speculative sprint when ALL
      of the currently active swarms in the sprint have all the workers they
      need (number of running (not mature) particles is _minParticlesPerSwarm).
      This means that we have capacity to run additional particles in a new
      swarm.

    It is expected that the sprints will be checked IN ORDER from 0 on up. (It
    is an error not to) The caller should always try to allocate from the first
    active sprint it finds. If it can't, then it can call this again to
    find/create the next active sprint.

    Parameters:
    ---------------------------------------------------------------------
    retval:   (active, noMoreSprints)
                active: True if the given sprint is active
                noMoreSprints: True if there are no more sprints possible
    """

    while True:
      numExistingSprints = len(self._state['sprints'])

      # If this sprint already exists, see if it is active
      if sprintIdx <= numExistingSprints-1:

        # With speculation off, it's simple, just return whether or not the
        #  asked for sprint has active status
        if not self._hsObj._speculativeParticles:
          active = (self._state['sprints'][sprintIdx]['status'] == 'active')
          return (active, False)

        # With speculation on, if the sprint is still marked active, we also
        #  need to see if it's time to add a new swarm to it.
        else:
          active = (self._state['sprints'][sprintIdx]['status'] == 'active')
          if not active:
            return (active, False)

          # See if all of the existing swarms are at capacity (have all the
          # workers they need):
          activeSwarmIds = self.getActiveSwarms(sprintIdx)
          swarmSizes = [self._hsObj._resultsDB.getParticleInfos(swarmId,
                              matured=False)[0] for swarmId in activeSwarmIds]
          notFullSwarms = [len(swarm) for swarm in swarmSizes \
                           if len(swarm) < self._hsObj._minParticlesPerSwarm]

          # If some swarms have room return that the swarm is active.
          if len(notFullSwarms) > 0:
            return (True, False)

          # If the existing swarms are at capacity, we will fall through to the
          #  logic below which tries to add a new swarm to the sprint.

      # Stop creating new sprints?
      if self._state['lastGoodSprint'] is not None:
        return (False, True)

      # if fixedFields is set, we are running a fast swarm and only run sprint0
      if self._hsObj._fixedFields is not None:
        return (False, True)

      # ----------------------------------------------------------------------
      # Get the best model (if there is one) from the prior sprint. That gives
      # us the base encoder set for the next sprint. For sprint zero make sure
      # it does not take the last sprintidx because of wrapping.
      if sprintIdx > 0  \
            and self._state['sprints'][sprintIdx-1]['status'] == 'completed':
        (bestModelId, _) = self.bestModelInCompletedSprint(sprintIdx-1)
        (particleState, _, _, _, _) = self._hsObj._resultsDB.getParticleInfo(
                                                                  bestModelId)
        bestSwarmId = particleState['swarmId']
        baseEncoderSets = [bestSwarmId.split('.')]

      # If there is no best model yet, then use all encoder sets from the prior
      #  sprint that were not killed
      else:
        bestSwarmId = None
        particleState = None
        # Build up more combinations, using ALL of the sets in the current
        #  sprint.
        baseEncoderSets = []
        for swarmId in self.getNonKilledSwarms(sprintIdx-1):
          baseEncoderSets.append(swarmId.split('.'))

      # ----------------------------------------------------------------------
      # Which encoders should we add to the current base set?
      encoderAddSet = []

      # If we have constraints on how many fields we carry forward into
      # subsequent sprints (either nupic.hypersearch.max.field.branching or
      # nupic.hypersearch.min.field.contribution was set), then be more
      # picky about which fields we add in.
      limitFields = False
      if self._hsObj._maxBranching > 0 \
            or self._hsObj._minFieldContribution >= 0:
        if self._hsObj._searchType == HsSearchType.temporal or \
            self._hsObj._searchType == HsSearchType.classification:
          if sprintIdx >= 1:
            limitFields = True
            baseSprintIdx = 0
        elif self._hsObj._searchType == HsSearchType.legacyTemporal:
          if sprintIdx >= 2:
            limitFields = True
            baseSprintIdx = 1
        else:
          raise RuntimeError("Unimplemented search type %s" % \
                                  (self._hsObj._searchType))


      # Only add top _maxBranching encoders to the swarms?
      if limitFields:

        # Get field contributions to filter added fields
        pctFieldContributions, absFieldContributions = \
                                                self.getFieldContributions()
        toRemove = []
        self.logger.debug("FieldContributions min: %s" % \
                          (self._hsObj._minFieldContribution))
        for fieldname in pctFieldContributions:
          if pctFieldContributions[fieldname] < self._hsObj._minFieldContribution:
            self.logger.debug("FieldContributions removing: %s" % (fieldname))
            toRemove.append(self.getEncoderKeyFromName(fieldname))
          else:
            self.logger.debug("FieldContributions keeping: %s" % (fieldname))


        # Grab the top maxBranching base sprint swarms.
        swarms = self._state["swarms"]
        sprintSwarms = [(swarm, swarms[swarm]["bestErrScore"]) \
            for swarm in swarms if swarms[swarm]["sprintIdx"] == baseSprintIdx]
        sprintSwarms = sorted(sprintSwarms, key=itemgetter(1))
        if self._hsObj._maxBranching > 0:
          sprintSwarms = sprintSwarms[0:self._hsObj._maxBranching]

        # Create encoder set to generate further swarms.
        for swarm in sprintSwarms:
          swarmEncoders = swarm[0].split(".")
          for encoder in swarmEncoders:
            if not encoder in encoderAddSet:
              encoderAddSet.append(encoder)
        encoderAddSet = [encoder for encoder in encoderAddSet \
                         if not str(encoder) in toRemove]

      # If no limit on the branching or min contribution, simply use all of the
      # encoders.
      else:
        encoderAddSet = self._hsObj._encoderNames


      # -----------------------------------------------------------------------
      # Build up the new encoder combinations for the next sprint.
      newSwarmIds = set()

      # See if the caller wants to try more extensive field combinations with
      #  3 fields.
      if (self._hsObj._searchType == HsSearchType.temporal \
           or self._hsObj._searchType == HsSearchType.legacyTemporal) \
          and sprintIdx == 2 \
          and (self._hsObj._tryAll3FieldCombinations or \
               self._hsObj._tryAll3FieldCombinationsWTimestamps):

        if self._hsObj._tryAll3FieldCombinations:
          newEncoders = set(self._hsObj._encoderNames)
          if self._hsObj._predictedFieldEncoder in newEncoders:
            newEncoders.remove(self._hsObj._predictedFieldEncoder)
        else:
          # Just make sure the timestamp encoders are part of the mix
          newEncoders = set(encoderAddSet)
          if self._hsObj._predictedFieldEncoder in newEncoders:
            newEncoders.remove(self._hsObj._predictedFieldEncoder)
          for encoder in self._hsObj._encoderNames:
            if encoder.endswith('_timeOfDay') or encoder.endswith('_weekend') \
                or encoder.endswith('_dayOfWeek'):
              newEncoders.add(encoder)

        allCombos = list(itertools.combinations(newEncoders, 2))
        for combo in allCombos:
          newSet = list(combo)
          newSet.append(self._hsObj._predictedFieldEncoder)
          newSet.sort()
          newSwarmId = '.'.join(newSet)
          if newSwarmId not in self._state['swarms']:
            newSwarmIds.add(newSwarmId)

            # If a speculative sprint, only add the first encoder, if not add
            #   all of them.
            if (len(self.getActiveSwarms(sprintIdx-1)) > 0):
              break

      # Else, we only build up by adding 1 new encoder to the best combination(s)
      #  we've seen from the prior sprint
      else:
        for baseEncoderSet in baseEncoderSets:
          for encoder in encoderAddSet:
            if encoder not in self._state['blackListedEncoders'] \
                and encoder not in baseEncoderSet:
              newSet = list(baseEncoderSet)
              newSet.append(encoder)
              newSet.sort()
              newSwarmId = '.'.join(newSet)
              if newSwarmId not in self._state['swarms']:
                newSwarmIds.add(newSwarmId)

                # If a speculative sprint, only add the first encoder, if not add
                #   all of them.
                if (len(self.getActiveSwarms(sprintIdx-1)) > 0):
                  break


      # ----------------------------------------------------------------------
      # Sort the new swarm Ids
      newSwarmIds = sorted(newSwarmIds)

      # If no more swarms can be found for this sprint...
      if len(newSwarmIds) == 0:
        # if sprint is not an empty sprint return that it is active but do not
        #  add anything to it.
        if len(self.getAllSwarms(sprintIdx)) > 0:
          return (True, False)

        # If this is an empty sprint and we couldn't find any new swarms to
        #   add (only bad fields are remaining), the search is over
        else:
          return (False, True)

      # Add this sprint and the swarms that are in it to our state
      self._dirty = True

      # Add in the new sprint if necessary
      if len(self._state["sprints"]) == sprintIdx:
        self._state['sprints'].append({'status': 'active',
                                       'bestModelId': None,
                                       'bestErrScore': None})

      # Add in the new swarm(s) to the sprint
      for swarmId in newSwarmIds:
        self._state['swarms'][swarmId] = {'status': 'active',
                                            'bestModelId': None,
                                            'bestErrScore': None,
                                            'sprintIdx': sprintIdx}

      # Update the list of active swarms
      self._state['activeSwarms'] = self.getActiveSwarms()

      # Try to set new state
      success = self.writeStateToDB()

      # Return result if successful
      if success:
        return (True, False)