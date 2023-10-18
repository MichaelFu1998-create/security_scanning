def getStats(self):
    """
    TODO: This method needs to be enhanced to get the stats on the *aggregated*
    records.

    :returns: stats (like min and max values of the fields).
    """

    # The record store returns a dict of stats, each value in this dict is
    #  a list with one item per field of the record store
    #         {
    #           'min' : [f1_min, f2_min, f3_min],
    #           'max' : [f1_max, f2_max, f3_max]
    #         }
    recordStoreStats = self._recordStore.getStats()

    # We need to convert each item to represent the fields of the *stream*
    streamStats = dict()
    for (key, values) in recordStoreStats.items():
      fieldStats = dict(zip(self._recordStoreFieldNames, values))
      streamValues = []
      for name in self._streamFieldNames:
        streamValues.append(fieldStats[name])
      streamStats[key] = streamValues

    return streamStats