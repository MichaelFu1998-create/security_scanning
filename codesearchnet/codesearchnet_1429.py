def getStats(self):
    """
    Parse the file using dedicated reader and collect fields stats. Never
    called if user of :class:`~.FileRecordStream` does not invoke
    :meth:`~.FileRecordStream.getStats` method.

    :returns:
          a dictionary of stats. In the current implementation, min and max
          fields are supported. Example of the return dictionary is:

          .. code-block:: python

             {
               'min' : [f1_min, f2_min, None, None, fn_min],
               'max' : [f1_max, f2_max, None, None, fn_max]
             }

          (where fx_min/fx_max are set for scalar fields, or None if not)

    """

    # Collect stats only once per File object, use fresh csv iterator
    # to keep the next() method returning sequential records no matter when
    # caller asks for stats
    if self._stats == None:
      # Stats are only available when reading csv file
      assert self._mode == self._FILE_READ_MODE

      inFile = open(self._filename, self._FILE_READ_MODE)

      # Create a new reader; read names, types, specials
      reader = csv.reader(inFile, dialect="excel")
      names = [n.strip() for n in reader.next()]
      types = [t.strip() for t in reader.next()]
      # Skip over specials
      reader.next()

      # Initialize stats to all None
      self._stats = dict()
      self._stats['min'] = []
      self._stats['max'] = []

      for i in xrange(len(names)):
        self._stats['min'].append(None)
        self._stats['max'].append(None)

      # Read the file, collect stats
      while True:
        try:
          line = reader.next()
          for i, f in enumerate(line):
            if (len(types) > i and
                types[i] in [FieldMetaType.integer, FieldMetaType.float] and
                f not in self._missingValues):
              value = self._adapters[i](f)
              if self._stats['max'][i] == None or \
                 self._stats['max'][i] < value:
                self._stats['max'][i] = value
              if self._stats['min'][i] == None or \
                 self._stats['min'][i] > value:
                self._stats['min'][i] = value

        except StopIteration:
          break

    return self._stats