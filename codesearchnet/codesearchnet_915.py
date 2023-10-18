def removeLabels(self, start=None, end=None, labelFilter=None):
    """
    Remove labels from each record with record ROWID in range from
    start to end, noninclusive of end. Removes all records if labelFilter is
    None, otherwise only removes the labels eqaul to labelFilter.

    This will recalculate all points from end to the last record stored in the
    internal cache of this classifier.
    """

    if len(self.saved_states) == 0:
      raise HTMPredictionModelInvalidRangeError("Invalid supplied range for "
        "'removeLabels'. Model has no saved records.")

    startID = self.saved_states[0].ROWID

    clippedStart = 0 if start is None else max(0, start - startID)
    clippedEnd = len(self.saved_states) if end is None else \
      max(0, min( len( self.saved_states) , end - startID))

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
            'endRecordID': self.saved_states[len(self.saved_states)-1].ROWID
          },
          'numRecordsStored': len(self.saved_states)
        })

    # Remove records within the cache
    recordsToDelete = []
    for state in self.saved_states[clippedStart:clippedEnd]:
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
    for state in self.saved_states[clippedEnd:]:
      self._updateState(state)

    return {'status': 'success'}