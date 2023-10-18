def generateStats(filename, statsInfo, maxSamples = None, filters=[], cache=True):
  """Generate requested statistics for a dataset and cache to a file.
  If filename is None, then don't cache to a file"""

  # Sanity checking
  if not isinstance(statsInfo, dict):
    raise RuntimeError("statsInfo must be a dict -- "
                       "found '%s' instead" % type(statsInfo))

  filename = resource_filename("nupic.datafiles", filename)

  if cache:
    statsFilename = getStatsFilename(filename, statsInfo, filters)
    # Use cached stats if found AND if it has the right data
    if os.path.exists(statsFilename):
      try:
        r = pickle.load(open(statsFilename, "rb"))
      except:
        # Ok to ignore errors -- we will just re-generate the file
        print "Warning: unable to load stats for %s -- " \
              "will regenerate" % filename
        r = dict()
      requestedKeys = set([s for s in statsInfo])
      availableKeys = set(r.keys())
      unavailableKeys = requestedKeys.difference(availableKeys)
      if len(unavailableKeys ) == 0:
        return r
      else:
        print "generateStats: re-generating stats file %s because " \
              "keys %s are not available" %  \
              (filename, str(unavailableKeys))
        os.remove(filename)

  print "Generating statistics for file '%s' with filters '%s'" % (filename, filters)
  sensor = RecordSensor()
  sensor.dataSource = FileRecordStream(filename)
  sensor.preEncodingFilters = filters

  # Convert collector description to collector object
  stats = []
  for field in statsInfo:
    # field = key from statsInfo
    if statsInfo[field] == "number":
      # This wants a field name e.g. consumption and the field type as the value
      statsInfo[field] = NumberStatsCollector()
    elif statsInfo[field] == "category":
      statsInfo[field] = CategoryStatsCollector()
    else:
      raise RuntimeError("Unknown stats type '%s' for field '%s'" % (statsInfo[field], field))

  # Now collect the stats
  if maxSamples is None:
    maxSamples = 500000
  for i in xrange(maxSamples):
    try:
      record = sensor.getNextRecord()
    except StopIteration:
      break
    for (name, collector) in statsInfo.items():
      collector.add(record[name])

  del sensor

  # Assemble the results and return
  r = dict()
  for (field, collector) in statsInfo.items():
    stats = collector.getStats()
    if field not in r:
      r[field] = stats
    else:
      r[field].update(stats)

  if cache:
    f = open(statsFilename, "wb")
    pickle.dump(r, f)
    f.close()
    # caller may need to know name of cached file
    r["_filename"] = statsFilename

  return r