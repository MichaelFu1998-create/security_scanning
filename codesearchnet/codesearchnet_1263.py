def getStats(self, stats):
    """ Override of getStats()  in BaseStatsCollector

        stats: A dictionary where all the stats are
        outputted

    """
    BaseStatsCollector.getStats(self, stats)

    sortedNumberList = sorted(self.valueList)
    listLength = len(sortedNumberList)
    min = sortedNumberList[0]
    max = sortedNumberList[-1]
    mean = numpy.mean(self.valueList)
    median = sortedNumberList[int(0.5*listLength)]
    percentile1st = sortedNumberList[int(0.01*listLength)]
    percentile99th = sortedNumberList[int(0.99*listLength)]

    differenceList = \
               [(cur - prev) for prev, cur in itertools.izip(list(self.valueSet)[:-1],
                                                             list(self.valueSet)[1:])]
    if min > max:
      print self.fieldname, min, max, '-----'
    meanResolution = numpy.mean(differenceList)


    stats[self.fieldname]['min'] = min
    stats[self.fieldname]['max'] = max
    stats[self.fieldname]['mean'] = mean
    stats[self.fieldname]['median'] = median
    stats[self.fieldname]['percentile1st'] = percentile1st
    stats[self.fieldname]['percentile99th'] = percentile99th
    stats[self.fieldname]['meanResolution'] = meanResolution

    # TODO: Right now, always pass the data along.
    # This is used for data-dependent encoders.
    passData = True
    if passData:
      stats[self.fieldname]['data'] = self.valueList

    if VERBOSITY > 2:
      print '--'
      print "Statistics:"
      print "min:", min
      print "max:", max
      print "mean:", mean
      print "median:", median
      print "1st percentile :", percentile1st
      print "99th percentile:", percentile99th

      print '--'
      print "Resolution:"
      print "Mean Resolution:", meanResolution

    if VERBOSITY > 3:
      print '--'
      print "Histogram:"
      counts, bins = numpy.histogram(self.valueList, new=True)
      print "Counts:", counts.tolist()
      print "Bins:", bins.tolist()