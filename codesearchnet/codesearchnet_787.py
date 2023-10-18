def addLabel(self, start, end, labelName):
    """
    Add the label labelName to each record with record ROWID in range from
    ``start`` to ``end``, noninclusive of end.

    This will recalculate all points from end to the last record stored in the
    internal cache of this classifier.

    :param start: (int) start index 
    :param end: (int) end index (noninclusive)
    :param labelName: (string) label name
    """
    if len(self._recordsCache) == 0:
      raise HTMPredictionModelInvalidRangeError("Invalid supplied range for 'addLabel'. "
        "Model has no saved records.")

    try:
      start = int(start)
    except Exception:
      start = 0

    try:
      end = int(end)
    except Exception:
      end = int(self._recordsCache[-1].ROWID)

    startID = self._recordsCache[0].ROWID

    clippedStart = max(0, start - startID)
    clippedEnd = max(0, min( len( self._recordsCache) , end - startID))

    if clippedEnd <= clippedStart:
      raise HTMPredictionModelInvalidRangeError("Invalid supplied range for 'addLabel'.",
                                                debugInfo={
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

    # Add label to range [clippedStart, clippedEnd)
    for state in self._recordsCache[clippedStart:clippedEnd]:
      if labelName not in state.anomalyLabel:
        state.anomalyLabel.append(labelName)
        state.setByUser = True
        self._addRecordToKNN(state)

    assert len(self.saved_categories) > 0

    # Recompute [end, ...)
    for state in self._recordsCache[clippedEnd:]:
      self._classifyState(state)