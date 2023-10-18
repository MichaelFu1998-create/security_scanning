def next(self, record, curInputBookmark):
    """ Return the next aggregated record, if any

    Parameters:
    ------------------------------------------------------------------------
    record:         The input record (values only) from the input source, or
                    None if the input has reached EOF (this will cause this
                    method to force completion of and return any partially
                    aggregated time period)
    curInputBookmark: The bookmark to the next input record
    retval:
      (outputRecord, inputBookmark)

      outputRecord: the aggregated record
      inputBookmark: a bookmark to the last position from the input that
                      contributed to this aggregated record.

      If we don't have any aggregated records yet, returns (None, None)


    The caller should generally do a loop like this:
      while True:
        inRecord = reader.getNextRecord()
        bookmark = reader.getBookmark()

        (aggRecord, aggBookmark) = aggregator.next(inRecord, bookmark)

        # reached EOF?
        if inRecord is None and aggRecord is None:
          break

        if aggRecord is not None:
          proessRecord(aggRecord, aggBookmark)


    This method makes use of the self._slice member variable to build up
    the values we need to aggregate. This is a dict of lists. The keys are
    the field indices and the elements of each list are the values for that
    field. For example:

      self._siice = { 0: [42, 53], 1: [4.0, 5.1] }

    """

    # This will hold the aggregated record we return
    outRecord = None

    # This will hold the bookmark of the last input used within the
    #  aggregated record we return.
    retInputBookmark = None

    if record is not None:

      # Increment input count
      self._inIdx += 1

      #print self._inIdx, record

      # Apply the filter, ignore the record if any field is unacceptable
      if self._filter != None and not self._filter[0](self._filter[1], record):
        return (None, None)

      # If no aggregation info just return as-is
      if self._nullAggregation:
        return (record, curInputBookmark)


      # ----------------------------------------------------------------------
      # Do aggregation

      #
      # Remember the very first record time stamp - it will be used as
      # the timestamp for all first records in all sequences to align
      # times for the aggregation/join of sequences.
      #
      # For a set of aggregated records, it will use the beginning of the time
      # window as a timestamp for the set
      #
      t = record[self._timeFieldIdx]

      if self._firstSequenceStartTime == None:
        self._firstSequenceStartTime = t

      # Create initial startTime and endTime if needed
      if self._startTime is None:
        self._startTime = t
      if self._endTime is None:
        self._endTime = self._getEndTime(t)
        assert self._endTime > t

      #print 'Processing line:', i, t, endTime
      #from dbgp.client import brk; brk(port=9011)


      # ----------------------------------------------------------------------
      # Does this record have a reset signal or sequence Id associated with it?
      # If so, see if we've reached a sequence boundary
      if self._resetFieldIdx is not None:
        resetSignal = record[self._resetFieldIdx]
      else:
        resetSignal = None

      if self._sequenceIdFieldIdx is not None:
        currSequenceId = record[self._sequenceIdFieldIdx]
      else:
        currSequenceId = None

      newSequence = (resetSignal == 1 and self._inIdx > 0) \
                      or self._sequenceId != currSequenceId \
                      or self._inIdx == 0

      if newSequence:
        self._sequenceId = currSequenceId


      # --------------------------------------------------------------------
      # We end the aggregation chunk if we go past the end time
      # -OR- we get an out of order record (t < startTime)
      sliceEnded = (t >= self._endTime or t < self._startTime)


      # -------------------------------------------------------------------
      # Time to generate a new output record?
      if (newSequence or sliceEnded) and len(self._slice) > 0:
        # Create aggregated record
        # print 'Creating aggregate record...'

        # Make first record timestamp as the beginning of the time period,
        # in case the first record wasn't falling on the beginning of the period
        for j, f in enumerate(self._fields):
          index = f[0]
          if index == self._timeFieldIdx:
            self._slice[j][0] = self._startTime
            break

        # Generate the aggregated record
        outRecord = self._createAggregateRecord()
        retInputBookmark = self._aggrInputBookmark

        # Reset the slice
        self._slice = defaultdict(list)


      # --------------------------------------------------------------------
      # Add current record to slice (Note keeping slices in memory). Each
      # field in the slice is a list of field values from all the sliced
      # records
      for j, f in enumerate(self._fields):
        index = f[0]
        # append the parsed field value to the proper aggregated slice field.
        self._slice[j].append(record[index])
        self._aggrInputBookmark = curInputBookmark


      # --------------------------------------------------------------------
      # If we've encountered a new sequence, start aggregation over again
      if newSequence:
        # TODO: May use self._firstSequenceStartTime as a start for the new
        # sequence (to align all sequences)
        self._startTime = t
        self._endTime = self._getEndTime(t)


      # --------------------------------------------------------------------
      # If a slice just ended, re-compute the start and end time for the
      #  next aggregated record
      if sliceEnded:
        # Did we receive an out of order record? If so, go back and iterate
        #   till we get to the next end time boundary.
        if t < self._startTime:
          self._endTime = self._firstSequenceStartTime
        while t >= self._endTime:
          self._startTime = self._endTime
          self._endTime = self._getEndTime(self._endTime)


      # If we have a record to return, do it now
      if outRecord is not None:
        return (outRecord, retInputBookmark)


    # ---------------------------------------------------------------------
    # Input reached EOF
    # Aggregate one last time in the end if necessary
    elif self._slice:

      # Make first record timestamp as the beginning of the time period,
      # in case the first record wasn't falling on the beginning of the period
      for j, f in enumerate(self._fields):
        index = f[0]
        if index == self._timeFieldIdx:
          self._slice[j][0] = self._startTime
          break

      outRecord = self._createAggregateRecord()
      retInputBookmark = self._aggrInputBookmark

      self._slice = defaultdict(list)


    # Return aggregated record
    return (outRecord, retInputBookmark)