def runNetwork(network, writer):
  """Run the network and write output to writer.

  :param network: a Network instance to run
  :param writer: a csv.writer instance to write output to
  """
  identityRegion = network.regions["identityRegion"]

  for i in xrange(_NUM_RECORDS):
    # Run the network for a single iteration
    network.run(1)

    # Write out the record number and encoding
    encoding = identityRegion.getOutputData("out")
    writer.writerow((i, encoding))