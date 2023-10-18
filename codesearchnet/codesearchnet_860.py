def readStateFromDB(self):
    """Set our state to that obtained from the engWorkerState field of the
    job record.


    Parameters:
    ---------------------------------------------------------------------
    stateJSON:    JSON encoded state from job record

    """
    self._priorStateJSON = self._hsObj._cjDAO.jobGetFields(self._hsObj._jobID,
                                                    ['engWorkerState'])[0]

    # Init if no prior state yet
    if self._priorStateJSON is None:
      swarms = dict()

      # Fast Swarm, first and only sprint has one swarm for each field
      # in fixedFields
      if self._hsObj._fixedFields is not None:
        print self._hsObj._fixedFields
        encoderSet = []
        for field in self._hsObj._fixedFields:
            if field =='_classifierInput':
              continue
            encoderName = self.getEncoderKeyFromName(field)
            assert encoderName in self._hsObj._encoderNames, "The field '%s' " \
              " specified in the fixedFields list is not present in this " \
              " model." % (field)
            encoderSet.append(encoderName)
        encoderSet.sort()
        swarms['.'.join(encoderSet)] = {
                                'status': 'active',
                                'bestModelId': None,
                                'bestErrScore': None,
                                'sprintIdx': 0,
                                }
      # Temporal prediction search, first sprint has N swarms of 1 field each,
      #  the predicted field may or may not be that one field.
      elif self._hsObj._searchType == HsSearchType.temporal:
        for encoderName in self._hsObj._encoderNames:
          swarms[encoderName] = {
                                  'status': 'active',
                                  'bestModelId': None,
                                  'bestErrScore': None,
                                  'sprintIdx': 0,
                                  }


      # Classification prediction search, first sprint has N swarms of 1 field
      #  each where this field can NOT be the predicted field.
      elif self._hsObj._searchType == HsSearchType.classification:
        for encoderName in self._hsObj._encoderNames:
          if encoderName == self._hsObj._predictedFieldEncoder:
            continue
          swarms[encoderName] = {
                                  'status': 'active',
                                  'bestModelId': None,
                                  'bestErrScore': None,
                                  'sprintIdx': 0,
                                  }

      # Legacy temporal. This is either a model that uses reconstruction or
      #  an older multi-step model that doesn't have a separate
      #  'classifierOnly' encoder for the predicted field. Here, the predicted
      #  field must ALWAYS be present and the first sprint tries the predicted
      #  field only
      elif self._hsObj._searchType == HsSearchType.legacyTemporal:
        swarms[self._hsObj._predictedFieldEncoder] = {
                       'status': 'active',
                       'bestModelId': None,
                       'bestErrScore': None,
                       'sprintIdx': 0,
                       }

      else:
        raise RuntimeError("Unsupported search type: %s" % \
                            (self._hsObj._searchType))

      # Initialize the state.
      self._state = dict(
        # The last time the state was updated by a worker.
        lastUpdateTime = time.time(),

        # Set from within setSwarmState() if we detect that the sprint we just
        #  completed did worse than a prior sprint. This stores the index of
        #  the last good sprint.
        lastGoodSprint = None,

        # Set from within setSwarmState() if lastGoodSprint is True and all
        #  sprints have completed.
        searchOver = False,

        # This is a summary of the active swarms - this information can also
        #  be obtained from the swarms entry that follows, but is summarized here
        #  for easier reference when viewing the state as presented by
        #  log messages and prints of the hsState data structure (by
        #  permutations_runner).
        activeSwarms = swarms.keys(),

        # All the swarms that have been created so far.
        swarms = swarms,

        # All the sprints that have completed or are in progress.
        sprints = [{'status': 'active',
                    'bestModelId': None,
                    'bestErrScore': None}],

        # The list of encoders we have "blacklisted" because they
        #  performed so poorly.
        blackListedEncoders = [],
        )

      # This will do nothing if the value of engWorkerState is not still None.
      self._hsObj._cjDAO.jobSetFieldIfEqual(
          self._hsObj._jobID, 'engWorkerState', json.dumps(self._state), None)

      self._priorStateJSON = self._hsObj._cjDAO.jobGetFields(
          self._hsObj._jobID, ['engWorkerState'])[0]
      assert (self._priorStateJSON is not None)

    # Read state from the database
    self._state = json.loads(self._priorStateJSON)
    self._dirty = False