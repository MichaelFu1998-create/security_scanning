def _updateSequenceInfo(self, r):
    """Keep track of sequence and make sure time goes forward

    Check if the current record is the beginning of a new sequence
    A new sequence starts in 2 cases:

    1. The sequence id changed (if there is a sequence id field)
    2. The reset field is 1 (if there is a reset field)

    Note that if there is no sequenceId field or resetId field then the entire
    dataset is technically one big sequence. The function will not return True
    for the first record in this case. This is Ok because it is important to
    detect new sequences only when there are multiple sequences in the file.
    """

    # Get current sequence id (if any)
    newSequence = False
    sequenceId = (r[self._sequenceIdIdx]
                  if self._sequenceIdIdx is not None else None)
    if sequenceId != self._currSequence:
      # verify that the new sequence didn't show up before
      if sequenceId in self._sequences:
        raise Exception('Broken sequence: %s, record: %s' % \
                        (sequenceId, r))

      # add the finished sequence to the set of sequence
      self._sequences.add(self._currSequence)
      self._currSequence = sequenceId

      # Verify that the reset is consistent (if there is one)
      if self._resetIdx:
        assert r[self._resetIdx] == 1
      newSequence = True

    else:
      # Check the reset
      reset = False
      if self._resetIdx:
        reset = r[self._resetIdx]
        if reset == 1:
          newSequence = True

    # If it's still the same old sequence make sure the time flows forward
    if not newSequence:
      if self._timeStampIdx and self._currTime is not None:
        t = r[self._timeStampIdx]
        if t < self._currTime:
          raise Exception('No time travel. Early timestamp for record: %s' % r)

    if self._timeStampIdx:
      self._currTime = r[self._timeStampIdx]