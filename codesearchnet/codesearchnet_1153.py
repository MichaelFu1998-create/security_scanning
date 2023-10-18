def getNextRecord(self):
    """ Returns combined data from all sources (values only).

    :returns: None on EOF; empty sequence on timeout.
    """


    # Keep reading from the raw input till we get enough for an aggregated
    #  record
    while True:

      # Reached EOF due to lastRow constraint?
      if self._sourceLastRecordIdx is not None  and \
          self._recordStore.getNextRecordIdx() >= self._sourceLastRecordIdx:
        preAggValues = None                             # indicates EOF
        bookmark = self._recordStore.getBookmark()

      else:
        # Get the raw record and bookmark
        preAggValues = self._recordStore.getNextRecord()
        bookmark = self._recordStore.getBookmark()

      if preAggValues == ():  # means timeout error occurred
        if self._eofOnTimeout:
          preAggValues = None  # act as if we got EOF
        else:
          return preAggValues  # Timeout indicator

      self._logger.debug('Read source record #%d: %r',
                        self._recordStore.getNextRecordIdx()-1, preAggValues)

      # Perform aggregation
      (fieldValues, aggBookmark) = self._aggregator.next(preAggValues, bookmark)

      # Update the aggregated record bookmark if we got a real record back
      if fieldValues is not None:
        self._aggBookmark = aggBookmark

      # Reached EOF?
      if preAggValues is None and fieldValues is None:
        return None

      # Return it if we have a record
      if fieldValues is not None:
        break


    # Do we need to re-order the fields in the record?
    if self._needFieldsFiltering:
      values = []
      srcDict = dict(zip(self._recordStoreFieldNames, fieldValues))
      for name in self._streamFieldNames:
        values.append(srcDict[name])
      fieldValues = values


    # Write to debug output?
    if self._writer is not None:
      self._writer.appendRecord(fieldValues)

    self._recordCount += 1

    self._logger.debug('Returning aggregated record #%d from getNextRecord(): '
                      '%r. Bookmark: %r',
                      self._recordCount-1, fieldValues, self._aggBookmark)
    return fieldValues