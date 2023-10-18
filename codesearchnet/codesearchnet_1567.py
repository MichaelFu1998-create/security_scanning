def _createPeriodicActivities(self):
    """Creates and returns a list of activites for this TaskRunner instance

    Returns: a list of PeriodicActivityRequest elements
    """
    # Initialize periodic activities
    periodicActivities = []

    # Metrics reporting
    class MetricsReportCb(object):
      def __init__(self, taskRunner):
        self.__taskRunner = taskRunner
        return

      def __call__(self):
        self.__taskRunner._getAndEmitExperimentMetrics()

    reportMetrics = PeriodicActivityRequest(
      repeating=True,
      period=1000,
      cb=MetricsReportCb(self))

    periodicActivities.append(reportMetrics)

    # Iteration progress
    class IterationProgressCb(object):
      PROGRESS_UPDATE_PERIOD_TICKS = 1000

      def __init__(self, taskLabel, requestedIterationCount, logger):
        self.__taskLabel = taskLabel
        self.__requestedIterationCount = requestedIterationCount
        self.__logger = logger

        self.__numIterationsSoFar = 0

      def __call__(self):
        self.__numIterationsSoFar += self.PROGRESS_UPDATE_PERIOD_TICKS
        self.__logger.debug("%s: ITERATION PROGRESS: %s of %s" % (
                              self.__taskLabel,
                              self.__numIterationsSoFar,
                              self.__requestedIterationCount))

    iterationProgressCb = IterationProgressCb(
      taskLabel=self.__task['taskLabel'],
      requestedIterationCount=self.__task['iterationCount'],
      logger=self.__logger)
    iterationProgressReporter = PeriodicActivityRequest(
      repeating=True,
      period=IterationProgressCb.PROGRESS_UPDATE_PERIOD_TICKS,
      cb=iterationProgressCb)

    periodicActivities.append(iterationProgressReporter)

    return periodicActivities