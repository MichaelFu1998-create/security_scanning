def generateDataset(aggregationInfo, inputFilename, outputFilename=None):
  """Generate a dataset of aggregated values

  Parameters:
  ----------------------------------------------------------------------------
  aggregationInfo: a dictionary that contains the following entries
    - fields: a list of pairs. Each pair is a field name and an
      aggregation function (e.g. sum). The function will be used to aggregate
      multiple values during the aggregation period.

  aggregation period: 0 or more of unit=value fields; allowed units are:
        [years months] |
        [weeks days hours minutes seconds milliseconds microseconds]
        NOTE: years and months are mutually-exclusive with the other units.
              See getEndTime() and _aggregate() for more details.
        Example1: years=1, months=6,
        Example2: hours=1, minutes=30,
        If none of the period fields are specified or if all that are specified
        have values of 0, then aggregation will be suppressed, and the given
        inputFile parameter value will be returned.

  inputFilename: filename of the input dataset within examples/prediction/data

  outputFilename: name for the output file. If not given, a name will be
        generated based on the input filename and the aggregation params

  retval: Name of the generated output file. This will be the same as the input
      file name if no aggregation needed to be performed



  If the input file contained a time field, sequence id field or reset field
  that were not specified in aggregationInfo fields, those fields will be
  added automatically with the following rules:

  1. The order will be R, S, T, rest of the fields
  2. The aggregation function for all will be to pick the first: lambda x: x[0]

    Returns: the path of the aggregated data file if aggregation was performed
      (in the same directory as the given input file); if aggregation did not
      need to be performed, then the given inputFile argument value is returned.
  """



  # Create the input stream
  inputFullPath = resource_filename("nupic.datafiles", inputFilename)
  inputObj = FileRecordStream(inputFullPath)


  # Instantiate the aggregator
  aggregator = Aggregator(aggregationInfo=aggregationInfo,
                          inputFields=inputObj.getFields())


  # Is it a null aggregation? If so, just return the input file unmodified
  if aggregator.isNullAggregation():
    return inputFullPath


  # ------------------------------------------------------------------------
  # If we were not given an output filename, create one based on the
  #  aggregation settings
  if outputFilename is None:
    outputFilename = 'agg_%s' % \
                        os.path.splitext(os.path.basename(inputFullPath))[0]
    timePeriods = 'years months weeks days '\
                  'hours minutes seconds milliseconds microseconds'
    for k in timePeriods.split():
      if aggregationInfo.get(k, 0) > 0:
        outputFilename += '_%s_%d' % (k, aggregationInfo[k])

    outputFilename += '.csv'
    outputFilename = os.path.join(os.path.dirname(inputFullPath), outputFilename)



  # ------------------------------------------------------------------------
  # If some other process already started creating this file, simply
  #   wait for it to finish and return without doing anything
  lockFilePath = outputFilename + '.please_wait'
  if os.path.isfile(outputFilename) or \
     os.path.isfile(lockFilePath):
    while os.path.isfile(lockFilePath):
      print 'Waiting for %s to be fully written by another process' % \
            lockFilePath
      time.sleep(1)
    return outputFilename


  # Create the lock file
  lockFD = open(lockFilePath, 'w')



  # -------------------------------------------------------------------------
  # Create the output stream
  outputObj = FileRecordStream(streamID=outputFilename, write=True,
                               fields=inputObj.getFields())


  # -------------------------------------------------------------------------
  # Write all aggregated records to the output
  while True:
    inRecord = inputObj.getNextRecord()

    (aggRecord, aggBookmark) = aggregator.next(inRecord, None)

    if aggRecord is None and inRecord is None:
      break

    if aggRecord is not None:
      outputObj.appendRecord(aggRecord)

  return outputFilename