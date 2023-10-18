def run(self):
    """ Runs the OPF Model

    Parameters:
    -------------------------------------------------------------------------
    retval:  (completionReason, completionMsg)
              where completionReason is one of the ClientJobsDAO.CMPL_REASON_XXX
                equates.
    """
    # -----------------------------------------------------------------------
    # Load the experiment's description.py module
    descriptionPyModule = helpers.loadExperimentDescriptionScriptFromDir(
      self._experimentDir)
    expIface = helpers.getExperimentDescriptionInterfaceFromModule(
      descriptionPyModule)
    expIface.normalizeStreamSources()

    modelDescription = expIface.getModelDescription()
    self._modelControl = expIface.getModelControl()

    # -----------------------------------------------------------------------
    # Create the input data stream for this task
    streamDef = self._modelControl['dataset']

    from nupic.data.stream_reader import StreamReader
    readTimeout = 0

    self._inputSource = StreamReader(streamDef, isBlocking=False,
                                     maxTimeout=readTimeout)


    # -----------------------------------------------------------------------
    #Get field statistics from the input source
    fieldStats = self._getFieldStats()
    # -----------------------------------------------------------------------
    # Construct the model instance
    self._model = ModelFactory.create(modelDescription)
    self._model.setFieldStatistics(fieldStats)
    self._model.enableLearning()
    self._model.enableInference(self._modelControl.get("inferenceArgs", None))

    # -----------------------------------------------------------------------
    # Instantiate the metrics
    self.__metricMgr = MetricsManager(self._modelControl.get('metrics',None),
                                      self._model.getFieldInfo(),
                                      self._model.getInferenceType())

    self.__loggedMetricPatterns = self._modelControl.get("loggedMetrics", [])

    self._optimizedMetricLabel = self.__getOptimizedMetricLabel()
    self._reportMetricLabels = matchPatterns(self._reportKeyPatterns,
                                              self._getMetricLabels())


    # -----------------------------------------------------------------------
    # Initialize periodic activities (e.g., for model result updates)
    self._periodic = self._initPeriodicActivities()

    # -----------------------------------------------------------------------
    # Create our top-level loop-control iterator
    numIters = self._modelControl.get('iterationCount', -1)

    # Are we asked to turn off learning for a certain # of iterations near the
    #  end?
    learningOffAt = None
    iterationCountInferOnly = self._modelControl.get('iterationCountInferOnly', 0)
    if iterationCountInferOnly == -1:
      self._model.disableLearning()
    elif iterationCountInferOnly > 0:
      assert numIters > iterationCountInferOnly, "when iterationCountInferOnly " \
        "is specified, iterationCount must be greater than " \
        "iterationCountInferOnly."
      learningOffAt = numIters - iterationCountInferOnly

    self.__runTaskMainLoop(numIters, learningOffAt=learningOffAt)

    # -----------------------------------------------------------------------
    # Perform final operations for model
    self._finalize()

    return (self._cmpReason, None)