def compute(self, inputs, outputs):
    """
    Get a record from the dataSource and encode it.
    
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.compute`.
    """
    if not self.topDownMode:
      data = self.getNextRecord()

      # The private keys in data are standard of RecordStreamIface objects. Any
      # add'l keys are column headers from the data source.
      reset = data["_reset"]
      sequenceId = data["_sequenceId"]
      categories = data["_category"]

      # Encode the processed records; populate outputs["dataOut"] in place
      self.encoder.encodeIntoArray(data, outputs["dataOut"])

      # If there is a field to predict, set bucketIdxOut and actValueOut.
      # There is a special case where a predicted field might be a vector, as in
      # the CoordinateEncoder. Since this encoder does not provide bucket
      # indices for prediction, we will ignore it.
      if self.predictedField is not None and self.predictedField != "vector":
        allEncoders = list(self.encoder.encoders)
        if self.disabledEncoder is not None:
          allEncoders.extend(self.disabledEncoder.encoders)
        encoders = [e for e in allEncoders
                    if e[0] == self.predictedField]
        if len(encoders) == 0:
          raise ValueError("There is no encoder for set for the predicted "
                           "field: %s" % self.predictedField)
        # TODO: Figure out why there are sometimes multiple encoders with the
        # same name.
        #elif len(encoders) > 1:
        #  raise ValueError("There cant' be more than 1 encoder for the "
        #                   "predicted field: %s" % self.predictedField)
        else:
          encoder = encoders[0][1]

        actualValue = data[self.predictedField]
        outputs["bucketIdxOut"][:] = encoder.getBucketIndices(actualValue)
        if isinstance(actualValue, str):
          outputs["actValueOut"][:] = encoder.getBucketIndices(actualValue)
        else:
          outputs["actValueOut"][:] = actualValue

      # Write out the scalar values obtained from they data source.
      outputs["sourceOut"][:] = self.encoder.getScalars(data)
      self._outputValues["sourceOut"] = self.encoder.getEncodedValues(data)

      # -----------------------------------------------------------------------
      # Get the encoded bit arrays for each field
      encoders = self.encoder.getEncoderList()
      prevOffset = 0
      sourceEncodings = []
      bitData = outputs["dataOut"]
      for encoder in encoders:
        nextOffset = prevOffset + encoder.getWidth()
        sourceEncodings.append(bitData[prevOffset:nextOffset])
        prevOffset = nextOffset
      self._outputValues['sourceEncodings'] = sourceEncodings

      # Execute post-encoding filters, if any
      for filter in self.postEncodingFilters:
        filter.process(encoder=self.encoder, data=outputs['dataOut'])

      # Populate the output numpy arrays; must assign by index.
      outputs['resetOut'][0] = reset
      outputs['sequenceIdOut'][0] = sequenceId
      self.populateCategoriesOut(categories, outputs['categoryOut'])

      # ------------------------------------------------------------------------
      # Verbose print?
      if self.verbosity >= 1:
        if self._iterNum == 0:
          self.encoder.pprintHeader(prefix="sensor:")
        if reset:
          print "RESET - sequenceID:%d" % sequenceId
        if self.verbosity >= 2:
          print

      # If verbosity >=2, print the record fields
      if self.verbosity >= 1:
        self.encoder.pprint(outputs["dataOut"], prefix="%7d:" % (self._iterNum))
        scalarValues = self.encoder.getScalars(data)
        nz = outputs["dataOut"].nonzero()[0]
        print "     nz: (%d)" % (len(nz)), nz
        print "  encIn:", self.encoder.scalarsToStr(scalarValues)
      if self.verbosity >= 2:
        # if hasattr(data, 'header'):
        #  header = data.header()
        # else:
        #  header = '     '.join(self.dataSource.names)
        # print "        ", header
        print "   data:", str(data)
      if self.verbosity >= 3:
        decoded = self.encoder.decode(outputs["dataOut"])
        print "decoded:", self.encoder.decodedToStr(decoded)

      self._iterNum += 1

    else:

      # ========================================================================
      # Spatial
      # ========================================================================
      # This is the top down compute in sensor

      # We get the spatial pooler's topDownOut as spatialTopDownIn
      spatialTopDownIn = inputs['spatialTopDownIn']
      spatialTopDownOut = self.encoder.topDownCompute(spatialTopDownIn)

      # -----------------------------------------------------------------------
      # Split topDownOutput into seperate outputs
      values = [elem.value for elem in spatialTopDownOut]
      scalars = [elem.scalar for elem in spatialTopDownOut]
      encodings = [elem.encoding for elem in spatialTopDownOut]
      self._outputValues['spatialTopDownOut'] = values
      outputs['spatialTopDownOut'][:] = numpy.array(scalars)
      self._outputValues['spatialTopDownEncodings'] = encodings

      # ========================================================================
      # Temporal
      # ========================================================================

      ## TODO: Add temporal top-down loop
      # We get the temporal memory's topDownOut passed through the spatial
      # pooler as temporalTopDownIn
      temporalTopDownIn = inputs['temporalTopDownIn']
      temporalTopDownOut = self.encoder.topDownCompute(temporalTopDownIn)

      # -----------------------------------------------------------------------
      # Split topDownOutput into separate outputs

      values = [elem.value for elem in temporalTopDownOut]
      scalars = [elem.scalar for elem in temporalTopDownOut]
      encodings = [elem.encoding for elem in temporalTopDownOut]
      self._outputValues['temporalTopDownOut'] = values
      outputs['temporalTopDownOut'][:] = numpy.array(scalars)
      self._outputValues['temporalTopDownEncodings'] = encodings

      assert len(spatialTopDownOut) == len(temporalTopDownOut), (
        "Error: spatialTopDownOut and temporalTopDownOut should be the same "
        "size")