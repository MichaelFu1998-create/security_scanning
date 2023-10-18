def getRuntimeStats(self):
    """
    Only returns data for a stat called ``numRunCalls``.
    :return:
    """
    ret = {"numRunCalls" : self.__numRunCalls}

    #--------------------------------------------------
    # Query temporal network stats
    temporalStats = dict()
    if self._hasTP:
      for stat in self._netInfo.statsCollectors:
        sdict = stat.getStats()
        temporalStats.update(sdict)

    ret[InferenceType.getLabel(InferenceType.TemporalNextStep)] = temporalStats


    return ret