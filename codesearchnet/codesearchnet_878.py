def runNetwork(network, writer):
  """Run the network and write output to writer.

  :param network: a Network instance to run
  :param writer: a csv.writer instance to write output to
  """
  sensorRegion = network.regions["sensor"]
  spatialPoolerRegion = network.regions["spatialPoolerRegion"]
  temporalPoolerRegion = network.regions["temporalPoolerRegion"]
  anomalyLikelihoodRegion = network.regions["anomalyLikelihoodRegion"]

  prevPredictedColumns = []

  for i in xrange(_NUM_RECORDS):
    # Run the network for a single iteration
    network.run(1)

    # Write out the anomaly likelihood along with the record number and consumption
    # value.
    consumption = sensorRegion.getOutputData("sourceOut")[0]
    anomalyScore = temporalPoolerRegion.getOutputData("anomalyScore")[0]
    anomalyLikelihood = anomalyLikelihoodRegion.getOutputData("anomalyLikelihood")[0]
    writer.writerow((i, consumption, anomalyScore, anomalyLikelihood))