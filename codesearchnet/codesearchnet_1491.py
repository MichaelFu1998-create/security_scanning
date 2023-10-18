def estimateAnomalyLikelihoods(anomalyScores,
                               averagingWindow=10,
                               skipRecords=0,
                               verbosity=0):
  """
  Given a series of anomaly scores, compute the likelihood for each score. This
  function should be called once on a bunch of historical anomaly scores for an
  initial estimate of the distribution. It should be called again every so often
  (say every 50 records) to update the estimate.

  :param anomalyScores: a list of records. Each record is a list with the
                        following three elements: [timestamp, value, score]

                        Example::

                            [datetime.datetime(2013, 8, 10, 23, 0), 6.0, 1.0]

                        For best results, the list should be between 1000
                        and 10,000 records
  :param averagingWindow: integer number of records to average over
  :param skipRecords: integer specifying number of records to skip when
                      estimating distributions. If skip records are >=
                      len(anomalyScores), a very broad distribution is returned
                      that makes everything pretty likely.
  :param verbosity: integer controlling extent of printouts for debugging

                      0 = none
                      1 = occasional information
                      2 = print every record

  :returns: 3-tuple consisting of:

            - likelihoods

              numpy array of likelihoods, one for each aggregated point

            - avgRecordList

              list of averaged input records

            - params

              a small JSON dict that contains the state of the estimator

  """
  if verbosity > 1:
    print("In estimateAnomalyLikelihoods.")
    print("Number of anomaly scores:", len(anomalyScores))
    print("Skip records=", skipRecords)
    print("First 20:", anomalyScores[0:min(20, len(anomalyScores))])

  if len(anomalyScores) == 0:
    raise ValueError("Must have at least one anomalyScore")

  # Compute averaged anomaly scores
  aggRecordList, historicalValues, total =  _anomalyScoreMovingAverage(
    anomalyScores,
    windowSize = averagingWindow,
    verbosity = verbosity)
  s = [r[2] for r in aggRecordList]
  dataValues = numpy.array(s)

  # Estimate the distribution of anomaly scores based on aggregated records
  if len(aggRecordList) <= skipRecords:
    distributionParams = nullDistribution(verbosity = verbosity)
  else:
    distributionParams = estimateNormal(dataValues[skipRecords:])

    # HACK ALERT! The HTMPredictionModel currently does not handle constant
    # metric values very well (time of day encoder changes sometimes lead to
    # unstable SDR's even though the metric is constant). Until this is
    # resolved, we explicitly detect and handle completely flat metric values by
    # reporting them as not anomalous.
    s = [r[1] for r in aggRecordList]
    # Only do this if the values are numeric
    if all([isinstance(r[1], numbers.Number) for r in aggRecordList]):
      metricValues = numpy.array(s)
      metricDistribution = estimateNormal(metricValues[skipRecords:],
                                          performLowerBoundCheck=False)

      if metricDistribution["variance"] < 1.5e-5:
        distributionParams = nullDistribution(verbosity = verbosity)

  # Estimate likelihoods based on this distribution
  likelihoods = numpy.array(dataValues, dtype=float)
  for i, s in enumerate(dataValues):
    likelihoods[i] = tailProbability(s, distributionParams)

  # Filter likelihood values
  filteredLikelihoods = numpy.array(
    _filterLikelihoods(likelihoods) )

  params = {
    "distribution":       distributionParams,
    "movingAverage": {
      "historicalValues": historicalValues,
      "total":            total,
      "windowSize":       averagingWindow,
    },
    "historicalLikelihoods":
      list(likelihoods[-min(averagingWindow, len(likelihoods)):]),
  }

  if verbosity > 1:
    print("Discovered params=")
    print(params)
    print("Number of likelihoods:", len(likelihoods))
    print("First 20 likelihoods:", (
      filteredLikelihoods[0:min(20, len(filteredLikelihoods))] ))
    print("leaving estimateAnomalyLikelihoods")


  return (filteredLikelihoods, aggRecordList, params)