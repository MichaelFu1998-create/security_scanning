def setAutoDetectWaitRecords(self, waitRecords):
    """
    Sets the autoDetectWaitRecords.
    """
    if not isinstance(waitRecords, int):
      raise HTMPredictionModelInvalidArgument("Invalid argument type \'%s\'. WaitRecord "
        "must be a number." % (type(waitRecords)))

    if len(self.saved_states) > 0 and waitRecords < self.saved_states[0].ROWID:
      raise HTMPredictionModelInvalidArgument("Invalid value. autoDetectWaitRecord value "
        "must be valid record within output stream. Current minimum ROWID in "
        "output stream is %d." % (self.saved_states[0].ROWID))

    self._autoDetectWaitRecords = waitRecords

    # Update all the states in the classifier's cache
    for state in self.saved_states:
      self._updateState(state)