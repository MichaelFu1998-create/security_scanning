def __openDatafile(self, modelResult):
    """Open the data file and write the header row"""

    # Write reset bit
    resetFieldMeta = FieldMetaInfo(
      name="reset",
      type=FieldMetaType.integer,
      special = FieldMetaSpecial.reset)

    self.__outputFieldsMeta.append(resetFieldMeta)


    # -----------------------------------------------------------------------
    # Write each of the raw inputs that go into the encoders
    rawInput = modelResult.rawInput
    rawFields = rawInput.keys()
    rawFields.sort()
    for field in rawFields:
      if field.startswith('_') or field == 'reset':
        continue
      value = rawInput[field]
      meta = FieldMetaInfo(name=field, type=FieldMetaType.string,
                           special=FieldMetaSpecial.none)
      self.__outputFieldsMeta.append(meta)
      self._rawInputNames.append(field)


    # -----------------------------------------------------------------------
    # Handle each of the inference elements
    for inferenceElement, value in modelResult.inferences.iteritems():
      inferenceLabel = InferenceElement.getLabel(inferenceElement)

      # TODO: Right now we assume list inferences are associated with
      # The input field metadata
      if type(value) in (list, tuple):
        # Append input and prediction field meta-info
        self.__outputFieldsMeta.extend(self.__getListMetaInfo(inferenceElement))

      elif isinstance(value, dict):
          self.__outputFieldsMeta.extend(self.__getDictMetaInfo(inferenceElement,
                                                                value))
      else:

        if InferenceElement.getInputElement(inferenceElement):
          self.__outputFieldsMeta.append(FieldMetaInfo(name=inferenceLabel+".actual",
                type=FieldMetaType.string, special = ''))
        self.__outputFieldsMeta.append(FieldMetaInfo(name=inferenceLabel,
                type=FieldMetaType.string, special = ''))

    if self.__metricNames:
      for metricName in self.__metricNames:
        metricField = FieldMetaInfo(
          name = metricName,
          type = FieldMetaType.float,
          special = FieldMetaSpecial.none)

        self.__outputFieldsMeta.append(metricField)

    # Create the inference directory for our experiment
    inferenceDir = _FileUtils.createExperimentInferenceDir(self.__experimentDir)

    # Consctruct the prediction dataset file path
    filename = (self.__label + "." +
                opf_utils.InferenceType.getLabel(self.__inferenceType) +
               ".predictionLog.csv")
    self.__datasetPath = os.path.join(inferenceDir, filename)

    # Create the output dataset
    print "OPENING OUTPUT FOR PREDICTION WRITER AT: %r" % self.__datasetPath
    print "Prediction field-meta: %r" % ([tuple(i) for i in self.__outputFieldsMeta],)
    self.__dataset = FileRecordStream(streamID=self.__datasetPath, write=True,
                                     fields=self.__outputFieldsMeta)

    # Copy data from checkpoint cache
    if self.__checkpointCache is not None:
      self.__checkpointCache.seek(0)

      reader = csv.reader(self.__checkpointCache, dialect='excel')

      # Skip header row
      try:
        header = reader.next()
      except StopIteration:
        print "Empty record checkpoint initializer for %r" % (self.__datasetPath,)
      else:
        assert tuple(self.__dataset.getFieldNames()) == tuple(header), \
          "dataset.getFieldNames(): %r; predictionCheckpointFieldNames: %r" % (
          tuple(self.__dataset.getFieldNames()), tuple(header))

      # Copy the rows from checkpoint
      numRowsCopied = 0
      while True:
        try:
          row = reader.next()
        except StopIteration:
          break

        #print "DEBUG: restoring row from checkpoint: %r" % (row,)

        self.__dataset.appendRecord(row)
        numRowsCopied += 1

      self.__dataset.flush()

      print "Restored %d rows from checkpoint for %r" % (
        numRowsCopied, self.__datasetPath)

      # Dispose of our checkpoint cache
      self.__checkpointCache.close()
      self.__checkpointCache = None

    return