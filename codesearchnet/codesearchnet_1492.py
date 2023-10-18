def updateAnomalyLikelihoods(anomalyScores,
                             params,
                             verbosity=0):
  """
  Compute updated probabilities for anomalyScores using the given params.

  :param anomalyScores: a list of records. Each record is a list with the
                        following three elements: [timestamp, value, score]

                        Example::

                            [datetime.datetime(2013, 8, 10, 23, 0), 6.0, 1.0]

  :param params: the JSON dict returned by estimateAnomalyLikelihoods
  :param verbosity: integer controlling extent of printouts for debugging
  :type verbosity: int

  :returns: 3-tuple consisting of:

            - likelihoods

              numpy array of likelihoods, one for each aggregated point

            - avgRecordList

              list of averaged input records

            - params

              an updated JSON object containing the state of this metric.

  """
  if verbosity > 3:
    print("In updateAnomalyLikelihoods.")
    print("Number of anomaly scores:", len(anomalyScores))
    print("First 20:", anomalyScores[0:min(20, len(anomalyScores))])
    print("Params:", params)

  if len(anomalyScores) == 0:
    raise ValueError("Must have at least one anomalyScore")

  if not isValidEstimatorParams(params):
    raise ValueError("'params' is not a valid params structure")

  # For backward compatibility.
  if "historicalLikelihoods" not in params:
    params["historicalLikelihoods"] = [1.0]

  # Compute moving averages of these new scores using the previous values
  # as well as likelihood for these scores using the old estimator
  historicalValues  = params["movingAverage"]["historicalValues"]
  total             = params["movingAverage"]["total"]
  windowSize        = params["movingAverage"]["windowSize"]

  aggRecordList = numpy.zeros(len(anomalyScores), dtype=float)
  likelihoods = numpy.zeros(len(anomalyScores), dtype=float)
  for i, v in enumerate(anomalyScores):
    newAverage, historicalValues, total = (
      MovingAverage.compute(historicalValues, total, v[2], windowSize)
    )
    aggRecordList[i] = newAverage
    likelihoods[i]   = tailProbability(newAverage, params["distribution"])

  # Filter the likelihood values. First we prepend the historical likelihoods
  # to the current set. Then we filter the values.  We peel off the likelihoods
  # to return and the last windowSize values to store for later.
  likelihoods2 = params["historicalLikelihoods"] + list(likelihoods)
  filteredLikelihoods = _filterLikelihoods(likelihoods2)
  likelihoods[:] = filteredLikelihoods[-len(likelihoods):]
  historicalLikelihoods = likelihoods2[-min(windowSize, len(likelihoods2)):]

  # Update the estimator
  newParams = {
    "distribution": params["distribution"],
    "movingAverage": {
      "historicalValues": historicalValues,
      "total": total,
      "windowSize": windowSize,
    },
    "historicalLikelihoods": historicalLikelihoods,
  }

  assert len(newParams["historicalLikelihoods"]) <= windowSize

  if verbosity > 3:
    print("Number of likelihoods:", len(likelihoods))
    print("First 20 likelihoods:", likelihoods[0:min(20, len(likelihoods))])
    print("Leaving updateAnomalyLikelihoods.")

  return (likelihoods, aggRecordList, newParams)