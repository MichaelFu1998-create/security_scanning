def runHotgym(numRecords):
  """Run the Hot Gym example."""

  # Create a data source for the network.
  dataSource = FileRecordStream(streamID=_INPUT_FILE_PATH)
  numRecords = min(numRecords, dataSource.getDataRowCount())
  network = createNetwork(dataSource)

  # Set predicted field
  network.regions["sensor"].setParameter("predictedField", "consumption")

  # Enable learning for all regions.
  network.regions["SP"].setParameter("learningMode", 1)
  network.regions["TM"].setParameter("learningMode", 1)
  network.regions["classifier"].setParameter("learningMode", 1)

  # Enable inference for all regions.
  network.regions["SP"].setParameter("inferenceMode", 1)
  network.regions["TM"].setParameter("inferenceMode", 1)
  network.regions["classifier"].setParameter("inferenceMode", 1)

  results = []
  N = 1  # Run the network, N iterations at a time.
  for iteration in range(0, numRecords, N):
    network.run(N)

    predictionResults = getPredictionResults(network, "classifier")
    oneStep = predictionResults[1]["predictedValue"]
    oneStepConfidence = predictionResults[1]["predictionConfidence"]
    fiveStep = predictionResults[5]["predictedValue"]
    fiveStepConfidence = predictionResults[5]["predictionConfidence"]

    result = (oneStep, oneStepConfidence * 100,
              fiveStep, fiveStepConfidence * 100)
    print "1-step: {:16} ({:4.4}%)\t 5-step: {:16} ({:4.4}%)".format(*result)
    results.append(result)

  return results