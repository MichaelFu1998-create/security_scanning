def _sortChunk(records, key, chunkIndex, fields):
  """Sort in memory chunk of records

  records - a list of records read from the original dataset
  key - a list of indices to sort the records by
  chunkIndex - the index of the current chunk

  The records contain only the fields requested by the user.

  _sortChunk() will write the sorted records to a standard File
  named "chunk_<chunk index>.csv" (chunk_0.csv, chunk_1.csv,...).
  """
  title(additional='(key=%s, chunkIndex=%d)' % (str(key), chunkIndex))

  assert len(records) > 0

  # Sort the current records
  records.sort(key=itemgetter(*key))

  # Write to a chunk file
  if chunkIndex is not None:
    filename = 'chunk_%d.csv' % chunkIndex
    with FileRecordStream(filename, write=True, fields=fields) as o:
      for r in records:
        o.appendRecord(r)

    assert os.path.getsize(filename) > 0

  return records