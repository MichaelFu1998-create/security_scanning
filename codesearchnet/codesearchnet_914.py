def addLabel(self, start, end, labelName):
    """
    Add the label labelName to each record with record ROWID in range from
    start to end, noninclusive of end.

    This will recalculate all points from end to the last record stored in the
    internal cache of this classifier.
    """
    if len(self.saved_states) == 0:
      raise HTMPredictionModelInvalidRangeError("Invalid supplied range for 'addLabel'. "
        "Model has no saved records.")

    startID = self.saved_states[0].ROWID

    clippedStart = max(0, start - startID)
    clippedEnd = max(0, min( len( self.saved_states) , end - startID))

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
            'endRecordID': self.saved_states[len(self.saved_states)-1].ROWID
          },
          'numRecordsStored': len(self.saved_states)
        })

    # Add label to range [clippedStart, clippedEnd)
    for state in self.saved_states[clippedStart:clippedEnd]:
      if labelName not in state.anomalyLabel:
        state.anomalyLabel.append(labelName)
        state.setByUser = True
        self._addRecordToKNN(state)

    assert len(self.saved_categories) > 0

    # Recompute [end, ...)
    for state in self.saved_states[clippedEnd:]:
      self._updateState(state)