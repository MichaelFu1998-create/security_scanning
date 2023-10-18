def read(cls, proto):
    """ capnp deserialization method for the anomaly likelihood object

    :param proto: (Object) capnp proto object specified in
                          nupic.regions.anomaly_likelihood.capnp

    :returns: (Object) the deserialized AnomalyLikelihood object
    """
    # pylint: disable=W0212
    anomalyLikelihood = object.__new__(cls)
    anomalyLikelihood._iteration = proto.iteration

    anomalyLikelihood._historicalScores = collections.deque(
      maxlen=proto.historicWindowSize)
    for i, score in enumerate(proto.historicalScores):
      anomalyLikelihood._historicalScores.append((i, score.value,
                                                  score.anomalyScore))
    if proto.distribution.name: # is "" when there is no distribution.
      anomalyLikelihood._distribution = dict()
      anomalyLikelihood._distribution['distribution'] = dict()
      anomalyLikelihood._distribution['distribution']["name"] = proto.distribution.name
      anomalyLikelihood._distribution['distribution']["mean"] = proto.distribution.mean
      anomalyLikelihood._distribution['distribution']["variance"] = proto.distribution.variance
      anomalyLikelihood._distribution['distribution']["stdev"] = proto.distribution.stdev

      anomalyLikelihood._distribution["movingAverage"] = {}
      anomalyLikelihood._distribution["movingAverage"]["windowSize"] = proto.distribution.movingAverage.windowSize
      anomalyLikelihood._distribution["movingAverage"]["historicalValues"] = []
      for value in proto.distribution.movingAverage.historicalValues:
        anomalyLikelihood._distribution["movingAverage"]["historicalValues"].append(value)
      anomalyLikelihood._distribution["movingAverage"]["total"] = proto.distribution.movingAverage.total

      anomalyLikelihood._distribution["historicalLikelihoods"] = []
      for likelihood in proto.distribution.historicalLikelihoods:
        anomalyLikelihood._distribution["historicalLikelihoods"].append(likelihood)
    else:
      anomalyLikelihood._distribution = None

    anomalyLikelihood._probationaryPeriod = proto.probationaryPeriod
    anomalyLikelihood._learningPeriod = proto.learningPeriod
    anomalyLikelihood._reestimationPeriod = proto.reestimationPeriod
    # pylint: enable=W0212

    return anomalyLikelihood