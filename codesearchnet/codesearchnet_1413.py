def applyFilters(self, data):
    """
    Apply pre-encoding filters. These filters may modify or add data. If a 
    filter needs another record (e.g. a delta filter) it will request another 
    record by returning False and the current record will be skipped (but will 
    still be given to all filters).

    We have to be very careful about resets. A filter may add a reset,
    but other filters should not see the added reset, each filter sees
    the original reset value, and we keep track of whether any filter
    adds a reset.

    :param data: (dict) The data that will be processed by the filter.
    :returns: (tuple) with the data processed by the filter and a boolean to
              know whether or not the filter needs mode data.
    """

    if self.verbosity > 0:
      print "RecordSensor got data: %s" % data

    allFiltersHaveEnoughData = True
    if len(self.preEncodingFilters) > 0:
      originalReset = data['_reset']
      actualReset = originalReset
      for f in self.preEncodingFilters:
        # if filter needs more data, it returns False
        filterHasEnoughData = f.process(data)
        allFiltersHaveEnoughData = (allFiltersHaveEnoughData
                                    and filterHasEnoughData)
        actualReset = actualReset or data['_reset']
        data['_reset'] = originalReset
      data['_reset'] = actualReset

    return data, allFiltersHaveEnoughData