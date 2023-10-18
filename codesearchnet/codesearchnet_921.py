def compute(self):
    """
    Run an iteration of this anomaly classifier
    """
    result = self._constructClassificationRecord()

    # Classify this point after waiting the classification delay
    if result.ROWID >= self._autoDetectWaitRecords:
      self._updateState(result)

    # Save new classification record and keep history as moving window
    self.saved_states.append(result)
    if len(self.saved_states) > self._history_length:
      self.saved_states.pop(0)

    return result