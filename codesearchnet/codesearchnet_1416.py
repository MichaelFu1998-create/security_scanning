def _convertNonNumericData(self, spatialOutput, temporalOutput, output):
    """
    Converts all of the non-numeric fields from spatialOutput and temporalOutput
    into their scalar equivalents and records them in the output dictionary.

    :param spatialOutput: The results of topDownCompute() for the spatial input.
    :param temporalOutput: The results of topDownCompute() for the temporal
      input.
    :param output: The main dictionary of outputs passed to compute(). It is
      expected to have keys 'spatialTopDownOut' and 'temporalTopDownOut' that
      are mapped to numpy arrays.
    """
    encoders = self.encoder.getEncoderList()
    types = self.encoder.getDecoderOutputFieldTypes()
    for i, (encoder, type) in enumerate(zip(encoders, types)):
      spatialData = spatialOutput[i]
      temporalData = temporalOutput[i]

      if type != FieldMetaType.integer and type != FieldMetaType.float:
        # TODO: Make sure that this doesn't modify any state
        spatialData = encoder.getScalars(spatialData)[0]
        temporalData = encoder.getScalars(temporalData)[0]

      assert isinstance(spatialData, (float, int))
      assert isinstance(temporalData, (float, int))
      output['spatialTopDownOut'][i] = spatialData
      output['temporalTopDownOut'][i] = temporalData