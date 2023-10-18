def _readPermutationsFile(self, filename, modelDescription):
    """
    Read the permutations file and initialize the following member variables:
        _predictedField: field name of the field we are trying to
          predict
        _permutations: Dict containing the full permutations dictionary.
        _flattenedPermutations: Dict containing the flattened version of
          _permutations. The keys leading to the value in the dict are joined
          with a period to create the new key and permute variables within
          encoders are pulled out of the encoder.
        _encoderNames: keys from self._permutations of only the encoder
          variables.
        _reportKeys:   The 'report' list from the permutations file.
          This is a list of the items from each experiment's pickled
          results file that should be included in the final report. The
          format of each item is a string of key names separated by colons,
          each key being one level deeper into the experiment results
          dict. For example, 'key1:key2'.
        _filterFunc: a user-supplied function that can be used to
          filter out specific permutation combinations.
        _optimizeKey: which report key to optimize for
        _maximize: True if we should try and maximize the optimizeKey
          metric. False if we should minimize it.
        _dummyModelParamsFunc: a user-supplied function that can be used to
          artificially generate HTMPredictionModel results. When supplied,
          the model is not actually run through the OPF, but instead is run
          through a "Dummy Model" (nupic.swarming.ModelRunner.
          OPFDummyModelRunner). This function returns the params dict used
          to control various options in the dummy model (the returned metric,
          the execution time, etc.). This is used for hypersearch algorithm
          development.

    Parameters:
    ---------------------------------------------------------
    filename:     Name of permutations file
    retval:       None
    """
    # Open and execute the permutations file
    vars = {}

    permFile = execfile(filename, globals(), vars)


    # Read in misc info.
    self._reportKeys = vars.get('report', [])
    self._filterFunc = vars.get('permutationFilter', None)
    self._dummyModelParamsFunc = vars.get('dummyModelParams', None)
    self._predictedField = None   # default
    self._predictedFieldEncoder = None   # default
    self._fixedFields = None # default

    # The fastSwarm variable, if present, contains the params from a best
    #  model from a previous swarm. If present, use info from that to seed
    #  a fast swarm
    self._fastSwarmModelParams = vars.get('fastSwarmModelParams', None)
    if self._fastSwarmModelParams is not None:
      encoders = self._fastSwarmModelParams['structuredParams']['modelParams']\
                  ['sensorParams']['encoders']
      self._fixedFields = []
      for fieldName in encoders:
        if encoders[fieldName] is not None:
          self._fixedFields.append(fieldName)

    if 'fixedFields' in vars:
      self._fixedFields = vars['fixedFields']

    # Get min number of particles per swarm from either permutations file or
    # config.
    self._minParticlesPerSwarm = vars.get('minParticlesPerSwarm')
    if self._minParticlesPerSwarm  == None:
      self._minParticlesPerSwarm = Configuration.get(
                                      'nupic.hypersearch.minParticlesPerSwarm')
    self._minParticlesPerSwarm = int(self._minParticlesPerSwarm)

    # Enable logic to kill off speculative swarms when an earlier sprint
    #  has found that it contains poorly performing field combination?
    self._killUselessSwarms = vars.get('killUselessSwarms', True)

    # The caller can request that the predicted field ALWAYS be included ("yes")
    #  or optionally include ("auto"). The setting of "no" is N/A and ignored
    #  because in that case the encoder for the predicted field will not even
    #  be present in the permutations file.
    # When set to "yes", this will force the first sprint to try the predicted
    #  field only (the legacy mode of swarming).
    # When set to "auto", the first sprint tries all possible fields (one at a
    #  time) in the first sprint.
    self._inputPredictedField = vars.get("inputPredictedField", "yes")

    # Try all possible 3-field combinations? Normally, we start with the best
    #  2-field combination as a base. When this flag is set though, we try
    #  all possible 3-field combinations which takes longer but can find a
    #  better model.
    self._tryAll3FieldCombinations = vars.get('tryAll3FieldCombinations', False)

    # Always include timestamp fields in the 3-field swarms?
    # This is a less compute intensive version of tryAll3FieldCombinations.
    # Instead of trying ALL possible 3 field combinations, it just insures
    # that the timestamp fields (dayOfWeek, timeOfDay, weekend) are never left
    # out when generating the 3-field swarms.
    self._tryAll3FieldCombinationsWTimestamps = vars.get(
                                'tryAll3FieldCombinationsWTimestamps', False)

    # Allow the permutations file to override minFieldContribution. This would
    #  be set to a negative number for large swarms so that you don't disqualify
    #  a field in an early sprint just because it did poorly there. Sometimes,
    #  a field that did poorly in an early sprint could help accuracy when
    #  added in a later sprint
    minFieldContribution = vars.get('minFieldContribution', None)
    if minFieldContribution is not None:
      self._minFieldContribution = minFieldContribution

    # Allow the permutations file to override maxBranching.
    maxBranching = vars.get('maxFieldBranching', None)
    if maxBranching is not None:
      self._maxBranching = maxBranching

    # Read in the optimization info.
    if 'maximize' in vars:
      self._optimizeKey = vars['maximize']
      self._maximize = True
    elif 'minimize' in vars:
      self._optimizeKey = vars['minimize']
      self._maximize = False
    else:
      raise RuntimeError("Permutations file '%s' does not include a maximize"
                         " or minimize metric.")

    # The permutations file is the new location for maxModels. The old location,
    #  in the jobParams is deprecated.
    maxModels = vars.get('maxModels')
    if maxModels is not None:
      if self._maxModels is None:
        self._maxModels = maxModels
      else:
        raise RuntimeError('It is an error to specify maxModels both in the job'
                ' params AND in the permutations file.')


    # Figure out if what kind of search this is:
    #
    #  If it's a temporal prediction search:
    #    the first sprint has 1 swarm, with just the predicted field
    #  elif it's a spatial prediction search:
    #    the first sprint has N swarms, each with predicted field + one
    #    other field.
    #  elif it's a classification search:
    #    the first sprint has N swarms, each with 1 field
    inferenceType = modelDescription['modelParams']['inferenceType']
    if not InferenceType.validate(inferenceType):
      raise ValueError("Invalid inference type %s" %inferenceType)

    if inferenceType in [InferenceType.TemporalMultiStep,
                         InferenceType.NontemporalMultiStep]:
      # If it does not have a separate encoder for the predicted field that
      #  goes to the classifier, it is a legacy multi-step network
      classifierOnlyEncoder = None
      for encoder in modelDescription["modelParams"]["sensorParams"]\
                    ["encoders"].values():
        if encoder.get("classifierOnly", False) \
             and encoder["fieldname"] == vars.get('predictedField', None):
          classifierOnlyEncoder = encoder
          break

      if classifierOnlyEncoder is None or self._inputPredictedField=="yes":
        # If we don't have a separate encoder for the classifier (legacy
        #  MultiStep) or the caller explicitly wants to include the predicted
        #  field, then use the legacy temporal search methodology.
        self._searchType = HsSearchType.legacyTemporal
      else:
        self._searchType = HsSearchType.temporal


    elif inferenceType in [InferenceType.TemporalNextStep,
                         InferenceType.TemporalAnomaly]:
      self._searchType = HsSearchType.legacyTemporal

    elif inferenceType in (InferenceType.TemporalClassification,
                            InferenceType.NontemporalClassification):
      self._searchType = HsSearchType.classification

    else:
      raise RuntimeError("Unsupported inference type: %s" % inferenceType)

    # Get the predicted field. Note that even classification experiments
    #  have a "predicted" field - which is the field that contains the
    #  classification value.
    self._predictedField = vars.get('predictedField', None)
    if self._predictedField is None:
      raise RuntimeError("Permutations file '%s' does not have the required"
                         " 'predictedField' variable" % filename)

    # Read in and validate the permutations dict
    if 'permutations' not in vars:
      raise RuntimeError("Permutations file '%s' does not define permutations" % filename)

    if not isinstance(vars['permutations'], dict):
      raise RuntimeError("Permutations file '%s' defines a permutations variable "
                         "but it is not a dict")

    self._encoderNames = []
    self._permutations = vars['permutations']
    self._flattenedPermutations = dict()
    def _flattenPermutations(value, keys):
      if ':' in keys[-1]:
        raise RuntimeError("The permutation variable '%s' contains a ':' "
                           "character, which is not allowed.")
      flatKey = _flattenKeys(keys)
      if isinstance(value, PermuteEncoder):
        self._encoderNames.append(flatKey)

        # If this is the encoder for the predicted field, save its name.
        if value.fieldName == self._predictedField:
          self._predictedFieldEncoder = flatKey

        # Store the flattened representations of the variables within the
        # encoder.
        for encKey, encValue in value.kwArgs.iteritems():
          if isinstance(encValue, PermuteVariable):
            self._flattenedPermutations['%s:%s' % (flatKey, encKey)] = encValue
      elif isinstance(value, PermuteVariable):
        self._flattenedPermutations[flatKey] = value


      else:
        if isinstance(value, PermuteVariable):
          self._flattenedPermutations[key] = value
    rApply(self._permutations, _flattenPermutations)