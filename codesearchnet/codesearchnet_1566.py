def run(self):
    """Runs a single experiment task"""
    self.__logger.debug("run(): Starting task <%s>", self.__task['taskLabel'])

    # Set up the task

    # Create our main loop-control iterator
    if self.__cmdOptions.privateOptions['testMode']:
      numIters = 10
    else:
      numIters = self.__task['iterationCount']

    if numIters >= 0:
      iterTracker = iter(xrange(numIters))
    else:
      iterTracker = iter(itertools.count())

    # Initialize periodic activities
    periodic = PeriodicActivityMgr(
      requestedActivities=self._createPeriodicActivities())

    # Reset sequence states in the model, so it starts looking for a new
    # sequence
    # TODO: should this be done in OPFTaskDriver.setup(), instead?  Is it always
    #       desired in Nupic?
    self.__model.resetSequenceStates()

    # Have Task Driver perform its initial setup activities, including setup
    # callbacks
    self.__taskDriver.setup()

    # Run it!
    while True:
      # Check controlling iterator first
      try:
        next(iterTracker)
      except StopIteration:
        break

      # Read next input record
      try:
        inputRecord = self.__datasetReader.next()
      except StopIteration:
        break

      # Process input record
      result = self.__taskDriver.handleInputRecord(inputRecord=inputRecord)

      if InferenceElement.encodings in result.inferences:
        result.inferences.pop(InferenceElement.encodings)
      self.__predictionLogger.writeRecord(result)

      # Run periodic activities
      periodic.tick()

    # Dump the experiment metrics at the end of the task
    self._getAndEmitExperimentMetrics(final=True)

    # Have Task Driver perform its final activities
    self.__taskDriver.finalize()

    # Reset sequence states in the model, so it starts looking for a new
    # sequence
    # TODO: should this be done in OPFTaskDriver.setup(), instead?  Is it always
    #       desired in Nupic?
    self.__model.resetSequenceStates()