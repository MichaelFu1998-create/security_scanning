def removeLabels(self, start=None, end=None, labelFilter=None):
    """
    Remove labels from each record with record ROWID in range from
    ``start`` to ``end``, noninclusive of end. Removes all records if 
    ``labelFilter`` is None, otherwise only removes the labels equal to 
    ``labelFilter``.

    This will recalculate all points from end to the last record stored in the
    internal cache of this classifier.
    
    :param start: (int) start index 
    :param end: (int) end index (noninclusive)
    :param labelFilter: (string) label filter
    """
    if len(self._recordsCache) == 0:
      raise HTMPredictionModelInvalidRangeError("Invalid supplied range for "
        "'removeLabels'. Model has no saved records.")

    try:
      start = int(start)
    except Exception:
      start = 0

    try:
      end = int(end)
    except Exception:
      end = self._recordsCache[-1].ROWID

    startID = self._recordsCache[0].ROWID

    clippedStart = 0 if start is None else max(0, start - startID)
    clippedEnd = len(self._recordsCache) if end is None else \
      max(0, min( len( self._recordsCache) , end - startID))

    if clippedEnd <= clippedStart:
      raise HTMPredictionModelInvalidRangeError("Invalid supplied range for "
        "'removeLabels'.", debugInfo={
          'requestRange': {
            'startRecordID': start,
            'endRecordID': end
          },
          'clippedRequestRange': {
            'startRecordID': clippedStart,
            'endRecordID': clippedEnd
          },
          'validRange': {
            'startRecordID': startID,
            'endRecordID': self._recordsCache[len(self._recordsCache)-1].ROWID
          },
          'numRecordsStored': len(self._recordsCache)
        })

    # Remove records within the cache
    recordsToDelete = []
    for state in self._recordsCache[clippedStart:clippedEnd]:
      if labelFilter is not None:
        if labelFilter in state.anomalyLabel:
          state.anomalyLabel.remove(labelFilter)
      else:
        state.anomalyLabel = []
      state.setByUser = False
      recordsToDelete.append(state)
    self._deleteRecordsFromKNN(recordsToDelete)

    # Remove records not in cache
    self._deleteRangeFromKNN(start, end)

    # Recompute [clippedEnd, ...)
    for state in self._recordsCache[clippedEnd:]:
      self._classifyState(state)