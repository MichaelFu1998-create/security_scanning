def _mergeFiles(key, chunkCount, outputFile, fields):
  """Merge sorted chunk files into a sorted output file

  chunkCount - the number of available chunk files
  outputFile the name of the sorted output file

  _mergeFiles()

  """
  title()

  # Open all chun files
  files = [FileRecordStream('chunk_%d.csv' % i) for i in range(chunkCount)]

  # Open output file
  with FileRecordStream(outputFile, write=True, fields=fields) as o:
    # Open all chunk files
    files = [FileRecordStream('chunk_%d.csv' % i) for i in range(chunkCount)]
    records = [f.getNextRecord() for f in files]

    # This loop will run until all files are exhausted
    while not all(r is None for r in records):
      # Cleanup None values (files that were exhausted)
      indices = [i for i,r in enumerate(records) if r is not None]
      records = [records[i] for i in indices]
      files = [files[i] for i in indices]

      # Find the current record
      r = min(records, key=itemgetter(*key))
      # Write it to the file
      o.appendRecord(r)

      # Find the index of file that produced the current record
      index = records.index(r)
      # Read a new record from the file
      records[index] = files[index].getNextRecord()

  # Cleanup chunk files
  for i, f in enumerate(files):
    f.close()
    os.remove('chunk_%d.csv' % i)