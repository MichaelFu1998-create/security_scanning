def createModels(self, numModels=1):
    """Create one or more new models for evaluation. These should NOT be models
    that we already know are in progress (i.e. those that have been sent to us
    via recordModelProgress). We return a list of models to the caller
    (HypersearchWorker) and if one can be successfully inserted into
    the models table (i.e. it is not a duplicate) then HypersearchWorker will
    turn around and call our runModel() method, passing in this model. If it
    is a duplicate, HypersearchWorker will call this method again. A model
    is a duplicate if either the  modelParamsHash or particleHash is
    identical to another entry in the model table.

    The numModels is provided by HypersearchWorker as a suggestion as to how
    many models to generate. This particular implementation only ever returns 1
    model.

    Before choosing some new models, we first do a sweep for any models that
    may have been abandonded by failed workers. If/when we detect an abandoned
    model, we mark it as complete and orphaned and hide it from any subsequent
    queries to our ResultsDB. This effectively considers it as if it never
    existed. We also change the paramsHash and particleHash in the model record
    of the models table so that we can create another model with the same
    params and particle status and run it (which we then do immediately).

    The modelParamsHash returned for each model should be a hash (max allowed
    size of ClientJobsDAO.hashMaxSize) that uniquely identifies this model by
    it's params and the optional particleHash should be a hash of the particleId
    and generation index. Every model that gets placed into the models database,
    either by this worker or another worker, will have these hashes computed for
    it. The recordModelProgress gets called for every model in the database and
    the hash is used to tell which, if any, are the same as the ones this worker
    generated.

    NOTE: We check first ourselves for possible duplicates using the paramsHash
    before we return a model. If HypersearchWorker failed to insert it (because
    some other worker beat us to it), it will turn around and call our
    recordModelProgress with that other model so that we now know about it. It
    will then call createModels() again.

    This methods returns an exit boolean and the model to evaluate. If there is
    no model to evalulate, we may return False for exit because we want to stay
    alive for a while, waiting for all other models to finish. This gives us
    a chance to detect and pick up any possibly orphaned model by another
    worker.

    Parameters:
    ----------------------------------------------------------------------
    numModels:   number of models to generate
    retval:      (exit, models)
                    exit: true if this worker should exit.
                    models: list of tuples, one for each model. Each tuple contains:
                      (modelParams, modelParamsHash, particleHash)

                 modelParams is a dictionary containing the following elements:

                   structuredParams: dictionary containing all variables for
                     this model, with encoders represented as a dict within
                     this dict (or None if they are not included.

                   particleState: dictionary containing the state of this
                     particle. This includes the position and velocity of
                     each of it's variables, the particleId, and the particle
                     generation index. It contains the following keys:

                     id: The particle Id of the particle we are using to
                           generate/track this model. This is a string of the
                           form <hypesearchWorkerId>.<particleIdx>
                     genIdx: the particle's generation index. This starts at 0
                           and increments every time we move the particle to a
                           new position.
                     swarmId: The swarmId, which is a string of the form
                       <encoder>.<encoder>... that describes this swarm
                     varStates: dict of the variable states. The key is the
                         variable name, the value is a dict of the variable's
                         position, velocity, bestPosition, bestResult, etc.
    """

    # Check for and mark orphaned models
    self._checkForOrphanedModels()

    modelResults = []
    for _ in xrange(numModels):
      candidateParticle = None

      # If we've reached the max # of model to evaluate, we're done.
      if (self._maxModels is not None and
          (self._resultsDB.numModels() - self._resultsDB.getNumErrModels()) >=
          self._maxModels):

        return (self._okToExit(), [])

      # If we don't already have a particle to work on, get a candidate swarm and
      # particle to work with. If None is returned for the particle it means
      # either that the search is over (if exitNow is also True) or that we need
      # to wait for other workers to finish up their models before we can pick
      # another particle to run (if exitNow is False).
      if candidateParticle is None:
        (exitNow, candidateParticle, candidateSwarm) = (
            self._getCandidateParticleAndSwarm())
      if candidateParticle is None:
        if exitNow:
          return (self._okToExit(), [])
        else:
          # Send an update status periodically to the JobTracker so that it doesn't
          # think this worker is dead.
          print >> sys.stderr, "reporter:status:In hypersearchV2: speculativeWait"
          time.sleep(self._speculativeWaitSecondsMax * random.random())
          return (False, [])
      useEncoders = candidateSwarm.split('.')
      numAttempts = 0

      # Loop until we can create a unique model that we haven't seen yet.
      while True:

        # If this is the Nth attempt with the same candidate, agitate it a bit
        # to find a new unique position for it.
        if numAttempts >= 1:
          self.logger.debug("Agitating particle to get unique position after %d "
                  "failed attempts in a row" % (numAttempts))
          candidateParticle.agitate()

        # Create the hierarchical params expected by the base description. Note
        # that this is where we incorporate encoders that have no permuted
        # values in them.
        position = candidateParticle.getPosition()
        structuredParams = dict()
        def _buildStructuredParams(value, keys):
          flatKey = _flattenKeys(keys)
          # If it's an encoder, either put in None if it's not used, or replace
          # all permuted constructor params with the actual position.
          if flatKey in self._encoderNames:
            if flatKey in useEncoders:
              # Form encoder dict, substituting in chosen permutation values.
              return value.getDict(flatKey, position)
            # Encoder not used.
            else:
              return None
          # Regular top-level variable.
          elif flatKey in position:
            return position[flatKey]
          # Fixed override of a parameter in the base description.
          else:
            return value

        structuredParams = rCopy(self._permutations,
                                           _buildStructuredParams,
                                           discardNoneKeys=False)

        # Create the modelParams.
        modelParams = dict(
                   structuredParams=structuredParams,
                   particleState = candidateParticle.getState()
                   )

        # And the hashes.
        m = hashlib.md5()
        m.update(sortedJSONDumpS(structuredParams))
        m.update(self._baseDescriptionHash)
        paramsHash = m.digest()

        particleInst = "%s.%s" % (modelParams['particleState']['id'],
                                  modelParams['particleState']['genIdx'])
        particleHash = hashlib.md5(particleInst).digest()

        # Increase attempt counter
        numAttempts += 1

        # If this is a new one, and passes the filter test, exit with it.
        # TODO: There is currently a problem with this filters implementation as
        # it relates to self._maxUniqueModelAttempts. When there is a filter in
        # effect, we should try a lot more times before we decide we have
        # exhausted the parameter space for this swarm. The question is, how many
        # more times?
        if self._filterFunc and not self._filterFunc(structuredParams):
          valid = False
        else:
          valid = True
        if valid and self._resultsDB.getModelIDFromParamsHash(paramsHash) is None:
          break

        # If we've exceeded the max allowed number of attempts, mark this swarm
        #  as completing or completed, so we don't try and allocate any more new
        #  particles to it, and pick another.
        if numAttempts >= self._maxUniqueModelAttempts:
          (exitNow, candidateParticle, candidateSwarm) \
                = self._getCandidateParticleAndSwarm(
                                              exhaustedSwarmId=candidateSwarm)
          if candidateParticle is None:
            if exitNow:
              return (self._okToExit(), [])
            else:
              time.sleep(self._speculativeWaitSecondsMax * random.random())
              return (False, [])
          numAttempts = 0
          useEncoders = candidateSwarm.split('.')

      # Log message
      if self.logger.getEffectiveLevel() <= logging.DEBUG:
        self.logger.debug("Submitting new potential model to HypersearchWorker: \n%s"
                       % (pprint.pformat(modelParams, indent=4)))
      modelResults.append((modelParams, paramsHash, particleHash))
    return (False, modelResults)