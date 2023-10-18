def runNetwork(network, writer):
  """Run the network and write output to writer.

  :param network: a Network instance to run
  :param writer: a csv.writer instance to write output to
  """
  sensorRegion = network.regions["sensor"]
  temporalPoolerRegion = network.regions["temporalPoolerRegion"]

  for i in xrange(_NUM_RECORDS):
    # Run the network for a single iteration
    network.run(1)

    # Write out the anomaly score along with the record number and consumption
    # value.
    anomalyScore = temporalPoolerRegion.getOutputData("anomalyScore")[0]
    consumption = sensorRegion.getOutputData("sourceOut")[0]
    writer.writerow((i, consumption, anomalyScore))