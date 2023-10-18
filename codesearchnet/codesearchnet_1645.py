def copy(reader, writer, start, stop, insertLocation=None, tsCol=None):
  """Copies a range of values to a new location in the data set.

  Args:
    reader: A FileRecordStream object with input data.
    writer: A FileRecordStream object to write output data to.
    start: The first row in the range to copy.
    stop: The last row in the range to copy.
    insertLocation: The location to insert the copied range. If not specified,
        the range is inserted immediately following itself.
  """
  assert stop >= start
  startRows = []
  copyRows = []
  ts = None
  inc = None
  if tsCol is None:
    tsCol = reader.getTimestampFieldIdx()
  for i, row in enumerate(reader):
    # Get the first timestamp and the increment.
    if ts is None:
      ts = row[tsCol]
    elif inc is None:
      inc = row[tsCol] - ts
    # Keep a list of all rows and a list of rows to copy.
    if i >= start and i <= stop:
      copyRows.append(row)
    startRows.append(row)
  # Insert the copied rows.
  if insertLocation is None:
    insertLocation = stop + 1
  startRows[insertLocation:insertLocation] = copyRows
  # Update the timestamps.
  for row in startRows:
    row[tsCol] = ts
    writer.appendRecord(row)
    ts += inc