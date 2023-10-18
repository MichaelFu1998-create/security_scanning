def encode(self, inputRow):
    """Encodes the given input row as a dict, with the
    keys being the field names. This also adds in some meta fields:
      '_category': The value from the category field (if any)
      '_reset': True if the reset field was True (if any)
      '_sequenceId': the value from the sequenceId field (if any)

    :param inputRow: sequence of values corresponding to a single input metric
      data row
    :rtype: dict
    """

    # Create the return dict
    result = dict(zip(self._fieldNames, inputRow))

    # Add in the special fields
    if self._categoryFieldIndex is not None:
      # category value can be an int or a list
      if isinstance(inputRow[self._categoryFieldIndex], int):
        result['_category'] = [inputRow[self._categoryFieldIndex]]
      else:
        result['_category'] = (inputRow[self._categoryFieldIndex]
                               if inputRow[self._categoryFieldIndex]
                               else [None])
    else:
      result['_category'] = [None]

    if self._resetFieldIndex is not None:
      result['_reset'] = int(bool(inputRow[self._resetFieldIndex]))
    else:
      result['_reset'] = 0

    if self._learningFieldIndex is not None:
      result['_learning'] = int(bool(inputRow[self._learningFieldIndex]))

    result['_timestampRecordIdx'] = None
    if self._timestampFieldIndex is not None:
      result['_timestamp'] = inputRow[self._timestampFieldIndex]
      # Compute the record index based on timestamp
      result['_timestampRecordIdx'] = self._computeTimestampRecordIdx(
        inputRow[self._timestampFieldIndex])
    else:
      result['_timestamp'] = None

    # -----------------------------------------------------------------------
    # Figure out the sequence ID
    hasReset = self._resetFieldIndex is not None
    hasSequenceId = self._sequenceFieldIndex is not None
    if hasReset and not hasSequenceId:
      # Reset only
      if result['_reset']:
        self._sequenceId += 1
      sequenceId = self._sequenceId

    elif not hasReset and hasSequenceId:
      sequenceId = inputRow[self._sequenceFieldIndex]
      result['_reset'] = int(sequenceId != self._sequenceId)
      self._sequenceId = sequenceId

    elif hasReset and hasSequenceId:
      sequenceId = inputRow[self._sequenceFieldIndex]

    else:
      sequenceId = 0

    if sequenceId is not None:
      result['_sequenceId'] = hash(sequenceId)
    else:
      result['_sequenceId'] = None

    return result