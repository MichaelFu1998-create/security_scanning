def _cacheSequenceInfoType(self):
    """Figure out whether reset, sequenceId,
    both or neither are present in the data.
    Compute once instead of every time.

    Taken from filesource.py"""

    hasReset = self.resetFieldName is not None
    hasSequenceId = self.sequenceIdFieldName is not None

    if hasReset and not hasSequenceId:
      self._sequenceInfoType = self.SEQUENCEINFO_RESET_ONLY
      self._prevSequenceId = 0
    elif not hasReset and hasSequenceId:
      self._sequenceInfoType = self.SEQUENCEINFO_SEQUENCEID_ONLY
      self._prevSequenceId = None
    elif hasReset and hasSequenceId:
      self._sequenceInfoType = self.SEQUENCEINFO_BOTH
    else:
      self._sequenceInfoType = self.SEQUENCEINFO_NONE