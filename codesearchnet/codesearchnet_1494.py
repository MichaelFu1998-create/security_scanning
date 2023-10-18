def _anomalyScoreMovingAverage(anomalyScores,
                               windowSize=10,
                               verbosity=0,
                              ):
  """
  Given a list of anomaly scores return a list of averaged records.
  anomalyScores is assumed to be a list of records of the form:
                [datetime.datetime(2013, 8, 10, 23, 0), 6.0, 1.0]

  Each record in the returned list list contains:
      [datetime, value, averagedScore]

  *Note:* we only average the anomaly score.
  """

  historicalValues = []
  total = 0.0
  averagedRecordList = []    # Aggregated records
  for record in anomalyScores:

    # Skip (but log) records without correct number of entries
    if not isinstance(record, (list, tuple)) or len(record) != 3:
      if verbosity >= 1:
        print("Malformed record:", record)
      continue

    avg, historicalValues, total = (
      MovingAverage.compute(historicalValues, total, record[2], windowSize)
      )

    averagedRecordList.append( [record[0], record[1], avg] )

    if verbosity > 2:
      print("Aggregating input record:", record)
      print("Result:", [record[0], record[1], avg])

  return averagedRecordList, historicalValues, total