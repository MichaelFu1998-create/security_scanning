def checkpoint(self, checkpointSink, maxRows):
    """ [virtual method override] Save a checkpoint of the prediction output
    stream. The checkpoint comprises up to maxRows of the most recent inference
    records.

    Parameters:
    ----------------------------------------------------------------------
    checkpointSink:     A File-like object where predictions checkpoint data, if
                        any, will be stored.
    maxRows:            Maximum number of most recent inference rows
                        to checkpoint.
    """

    checkpointSink.truncate()

    if self.__dataset is None:
      if self.__checkpointCache is not None:
        self.__checkpointCache.seek(0)
        shutil.copyfileobj(self.__checkpointCache, checkpointSink)
        checkpointSink.flush()
        return
      else:
        # Nothing to checkpoint
        return

    self.__dataset.flush()
    totalDataRows = self.__dataset.getDataRowCount()

    if totalDataRows == 0:
      # Nothing to checkpoint
      return

    # Open reader of prediction file (suppress missingValues conversion)
    reader = FileRecordStream(self.__datasetPath, missingValues=[])

    # Create CSV writer for writing checkpoint rows
    writer = csv.writer(checkpointSink)

    # Write the header row to checkpoint sink -- just field names
    writer.writerow(reader.getFieldNames())

    # Determine number of rows to checkpoint
    numToWrite = min(maxRows, totalDataRows)

    # Skip initial rows to get to the rows that we actually need to checkpoint
    numRowsToSkip = totalDataRows - numToWrite
    for i in xrange(numRowsToSkip):
      reader.next()

    # Write the data rows to checkpoint sink
    numWritten = 0
    while True:
      row = reader.getNextRecord()
      if row is None:
        break;

      row =  [str(element) for element in row]

      #print "DEBUG: _BasicPredictionWriter: checkpointing row: %r" % (row,)

      writer.writerow(row)

      numWritten +=1

    assert numWritten == numToWrite, \
      "numWritten (%s) != numToWrite (%s)" % (numWritten, numToWrite)


    checkpointSink.flush()

    return