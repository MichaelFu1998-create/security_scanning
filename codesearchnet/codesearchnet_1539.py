def getFilename(aggregationInfo, inputFile):
  """Generate the filename for aggregated dataset

  The filename is based on the input filename and the
  aggregation period.

  Returns the inputFile if no aggregation required (aggregation
  info has all 0's)
  """

  # Find the actual file, with an absolute path
  inputFile = resource_filename("nupic.datafiles", inputFile)

  a = defaultdict(lambda: 0, aggregationInfo)
  outputDir = os.path.dirname(inputFile)
  outputFile = 'agg_%s' % os.path.splitext(os.path.basename(inputFile))[0]
  noAggregation = True
  timePeriods = 'years months weeks days '\
                'hours minutes seconds milliseconds microseconds'
  for k in timePeriods.split():
    if a[k] > 0:
      noAggregation = False
      outputFile += '_%s_%d' % (k, a[k])

  if noAggregation:
    return inputFile
  outputFile += '.csv'
  outputFile = os.path.join(outputDir, outputFile)

  return outputFile