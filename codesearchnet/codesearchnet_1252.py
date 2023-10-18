def runNetwork(network, numRecords, writer):
  """
  Runs specified Network writing the ensuing anomaly
  scores to writer.

  @param network: The Network instance to be run
  @param writer: A csv.writer used to write to output file.
  """
  sensorRegion = network.regions[_RECORD_SENSOR]
  l1SpRegion = network.regions[_L1_SPATIAL_POOLER]
  l1TpRegion = network.regions[_L1_TEMPORAL_MEMORY]
  l1Classifier = network.regions[_L1_CLASSIFIER]

  l2SpRegion = network.regions[_L2_SPATIAL_POOLER]
  l2TpRegion = network.regions[_L2_TEMPORAL_MEMORY]
  l2Classifier = network.regions[_L2_CLASSIFIER]

  l1PreviousPredictedColumns = []
  l2PreviousPredictedColumns = []

  l1PreviousPrediction = None
  l2PreviousPrediction = None
  l1ErrorSum = 0.0
  l2ErrorSum = 0.0
  for record in xrange(numRecords):
    # Run the network for a single iteration
    network.run(1)

    actual = float(sensorRegion.getOutputData("actValueOut")[0])

    l1Predictions = l1Classifier.getOutputData("actualValues")
    l1Probabilities = l1Classifier.getOutputData("probabilities")
    l1Prediction = l1Predictions[l1Probabilities.argmax()]
    if l1PreviousPrediction is not None:
      l1ErrorSum += math.fabs(l1PreviousPrediction - actual)
    l1PreviousPrediction = l1Prediction

    l2Predictions = l2Classifier.getOutputData("actualValues")
    l2Probabilities = l2Classifier.getOutputData("probabilities")
    l2Prediction = l2Predictions[l2Probabilities.argmax()]
    if l2PreviousPrediction is not None:
      l2ErrorSum += math.fabs(l2PreviousPrediction - actual)
    l2PreviousPrediction = l2Prediction

    l1AnomalyScore = l1TpRegion.getOutputData("anomalyScore")[0]
    l2AnomalyScore = l2TpRegion.getOutputData("anomalyScore")[0]

    # Write record number, actualInput, and anomaly scores
    writer.writerow((record, actual, l1PreviousPrediction, l1AnomalyScore, l2PreviousPrediction, l2AnomalyScore))

    # Store the predicted columns for the next timestep
    l1PredictedColumns = l1TpRegion.getOutputData("topDownOut").nonzero()[0]
    l1PreviousPredictedColumns = copy.deepcopy(l1PredictedColumns)
    #
    l2PredictedColumns = l2TpRegion.getOutputData("topDownOut").nonzero()[0]
    l2PreviousPredictedColumns = copy.deepcopy(l2PredictedColumns)

  # Output absolute average error for each level
  if numRecords > 1:
    print "L1 ave abs class. error: %f" % (l1ErrorSum / (numRecords - 1))
    print "L2 ave abs class. error: %f" % (l2ErrorSum / (numRecords - 1))