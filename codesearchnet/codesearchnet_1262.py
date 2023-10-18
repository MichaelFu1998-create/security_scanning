def generateStats(filename, maxSamples = None,):
  """
  Collect statistics for each of the fields in the user input data file and
  return a stats dict object.

  Parameters:
  ------------------------------------------------------------------------------
  filename:             The path and name of the data file.
  maxSamples:           Upper bound on the number of rows to be processed
  retval:               A dictionary of dictionaries. The top level keys are the
                        field names and the corresponding values are the statistics
                        collected for the individual file.
                        Example:
                        {
                          'consumption':{'min':0,'max':90,'mean':50,...},
                          'gym':{'numDistinctCategories':10,...},
                          ...
                         }


  """
  # Mapping from field type to stats collector object
  statsCollectorMapping = {'float':    FloatStatsCollector,
                           'int':      IntStatsCollector,
                           'string':   StringStatsCollector,
                           'datetime': DateTimeStatsCollector,
                           'bool':     BoolStatsCollector,
                           }

  filename = resource_filename("nupic.datafiles", filename)
  print "*"*40
  print "Collecting statistics for file:'%s'" % (filename,)
  dataFile = FileRecordStream(filename)

  # Initialize collector objects
  # statsCollectors list holds statsCollector objects for each field
  statsCollectors = []
  for fieldName, fieldType, fieldSpecial in dataFile.getFields():
    # Find the corresponding stats collector for each field based on field type
    # and intialize an instance
    statsCollector = \
            statsCollectorMapping[fieldType](fieldName, fieldType, fieldSpecial)
    statsCollectors.append(statsCollector)

  # Now collect the stats
  if maxSamples is None:
    maxSamples = 500000
  for i in xrange(maxSamples):
    record = dataFile.getNextRecord()
    if record is None:
      break
    for i, value in enumerate(record):
      statsCollectors[i].addValue(value)

  # stats dict holds the statistics for each field
  stats = {}
  for statsCollector in statsCollectors:
    statsCollector.getStats(stats)

  # We don't want to include reset field in permutations
  # TODO: handle reset field in a clean way
  if dataFile.getResetFieldIdx() is not None:
    resetFieldName,_,_ = dataFile.getFields()[dataFile.reset]
    stats.pop(resetFieldName)

  if VERBOSITY > 0:
    pprint.pprint(stats)

  return stats