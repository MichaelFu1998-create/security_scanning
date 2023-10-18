def sort(filename, key, outputFile, fields=None, watermark=1024 * 1024 * 100):
  """Sort a potentially big file

  filename - the input file (standard File format)
  key - a list of field names to sort by
  outputFile - the name of the output file
  fields - a list of fields that should be included (all fields if None)
  watermark - when available memory goes bellow the watermark create a new chunk

  sort() works by reading as records from the file into memory
  and calling _sortChunk() on each chunk. In the process it gets
  rid of unneeded fields if any. Once all the chunks have been sorted and
  written to chunk files it calls _merge() to merge all the chunks into a
  single sorted file.

  Note, that sort() gets a key that contains field names, which it converts
  into field indices for _sortChunk() becuase _sortChunk() doesn't need to know
  the field name.

  sort() figures out by itself how many chunk files to use by reading records
  from the file until the low watermark value of availabel memory is hit and
  then it sorts the current records, generates a chunk file, clears the sorted
  records and starts on a new chunk.

  The key field names are turned into indices
  """
  if fields is not None:
    assert set(key).issubset(set([f[0] for f in fields]))

  with FileRecordStream(filename) as f:


    # Find the indices of the requested fields
    if fields:
      fieldNames = [ff[0] for ff in fields]
      indices = [f.getFieldNames().index(name) for name in fieldNames]
      assert len(indices) == len(fields)
    else:
      fileds = f.getFields()
      fieldNames = f.getFieldNames()
      indices = None

    # turn key fields to key indices
    key = [fieldNames.index(name) for name in key]

    chunk = 0
    records = []
    for i, r in enumerate(f):
      # Select requested fields only
      if indices:
        temp = []
        for i in indices:
          temp.append(r[i])
        r = temp
      # Store processed record
      records.append(r)

      # Check memory
      available_memory = psutil.avail_phymem()

      # If bellow the watermark create a new chunk, reset and keep going
      if available_memory < watermark:
        _sortChunk(records, key, chunk, fields)
        records = []
        chunk += 1

    # Sort and write the remainder
    if len(records) > 0:
      _sortChunk(records, key, chunk, fields)
      chunk += 1

    # Marge all the files
    _mergeFiles(key, chunk, outputFile, fields)