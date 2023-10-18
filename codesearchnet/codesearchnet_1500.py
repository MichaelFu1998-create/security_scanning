def write(self, proto):
    """ capnp serialization method for the anomaly likelihood object

    :param proto: (Object) capnp proto object specified in
                          nupic.regions.anomaly_likelihood.capnp
    """

    proto.iteration = self._iteration

    pHistScores = proto.init('historicalScores', len(self._historicalScores))
    for i, score in enumerate(list(self._historicalScores)):
      _, value, anomalyScore = score
      record = pHistScores[i]
      record.value = float(value)
      record.anomalyScore = float(anomalyScore)

    if self._distribution:
      proto.distribution.name = self._distribution["distribution"]["name"]
      proto.distribution.mean = float(self._distribution["distribution"]["mean"])
      proto.distribution.variance = float(self._distribution["distribution"]["variance"])
      proto.distribution.stdev = float(self._distribution["distribution"]["stdev"])

      proto.distribution.movingAverage.windowSize = float(self._distribution["movingAverage"]["windowSize"])

      historicalValues = self._distribution["movingAverage"]["historicalValues"]
      pHistValues = proto.distribution.movingAverage.init(
        "historicalValues", len(historicalValues))
      for i, value in enumerate(historicalValues):
        pHistValues[i] = float(value)

      #proto.distribution.movingAverage.historicalValues = self._distribution["movingAverage"]["historicalValues"]
      proto.distribution.movingAverage.total = float(self._distribution["movingAverage"]["total"])

      historicalLikelihoods = self._distribution["historicalLikelihoods"]
      pHistLikelihoods = proto.distribution.init("historicalLikelihoods",
                                                 len(historicalLikelihoods))
      for i, likelihood in enumerate(historicalLikelihoods):
        pHistLikelihoods[i] = float(likelihood)

    proto.probationaryPeriod = self._probationaryPeriod
    proto.learningPeriod = self._learningPeriod
    proto.reestimationPeriod = self._reestimationPeriod
    proto.historicWindowSize = self._historicalScores.maxlen