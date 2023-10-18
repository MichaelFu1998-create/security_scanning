def sample(reader, writer, n, start=None, stop=None, tsCol=None,
           writeSampleOnly=True):
  """Samples n rows.

  Args:
    reader: A FileRecordStream object with input data.
    writer: A FileRecordStream object to write output data to.
    n: The number of elements to sample.
    start: The first row in the range to sample from.
    stop: The last row in the range to sample from.
    tsCol: If specified, the timestamp column to update.
    writeSampleOnly: If False, the rows before start are written before the
        sample and the rows after stop are written after the sample.
  """
  rows = list(reader)
  if tsCol is not None:
    ts = rows[0][tsCol]
    inc = rows[1][tsCol] - ts
  if start is None:
    start = 0
  if stop is None:
    stop = len(rows) - 1
  initialN = stop - start + 1
  # Select random rows in the sample range to delete until the desired number
  # of rows are left.
  numDeletes =  initialN - n
  for i in xrange(numDeletes):
    delIndex = random.randint(start, stop - i)
    del rows[delIndex]
  # Remove outside rows if specified.
  if writeSampleOnly:
    rows = rows[start:start + n]
  # Rewrite columns if tsCol is given.
  if tsCol is not None:
    ts = rows[0][tsCol]
  # Write resulting rows.
  for row in rows:
    if tsCol is not None:
      row[tsCol] = ts
      ts += inc
    writer.appendRecord(row)