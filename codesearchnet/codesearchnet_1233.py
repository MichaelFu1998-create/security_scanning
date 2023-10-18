def append(self, modelResult):
    """ [virtual method override] Emits a single prediction as input versus
    predicted.

    modelResult:    An opf_utils.ModelResult object that contains the model input
                    and output for the current timestep.
    """

    #print "DEBUG: _BasicPredictionWriter: writing modelResult: %r" % (modelResult,)

    # If there are no inferences, don't write anything
    inferences = modelResult.inferences
    hasInferences = False
    if inferences is not None:
      for value in inferences.itervalues():
        hasInferences = hasInferences or (value is not None)

    if not hasInferences:
      return

    if self.__dataset is None:
      self.__openDatafile(modelResult)

    inputData = modelResult.sensorInput

    sequenceReset = int(bool(inputData.sequenceReset))
    outputRow = [sequenceReset]


    # -----------------------------------------------------------------------
    # Write out the raw inputs
    rawInput = modelResult.rawInput
    for field in self._rawInputNames:
      outputRow.append(str(rawInput[field]))

    # -----------------------------------------------------------------------
    # Write out the inference element info
    for inferenceElement, outputVal in inferences.iteritems():
      inputElement = InferenceElement.getInputElement(inferenceElement)
      if inputElement:
        inputVal = getattr(inputData, inputElement)
      else:
        inputVal = None

      if type(outputVal) in (list, tuple):
        assert type(inputVal) in (list, tuple, None)

        for iv, ov in zip(inputVal, outputVal):
          # Write actual
          outputRow.append(str(iv))

          # Write inferred
          outputRow.append(str(ov))
      elif isinstance(outputVal, dict):
        if inputVal is not None:
          # If we have a predicted field, include only that in the actuals
          if modelResult.predictedFieldName is not None:
            outputRow.append(str(inputVal[modelResult.predictedFieldName]))
          else:
            outputRow.append(str(inputVal))
        for key in sorted(outputVal.keys()):
          outputRow.append(str(outputVal[key]))
      else:
        if inputVal is not None:
          outputRow.append(str(inputVal))
        outputRow.append(str(outputVal))

    metrics = modelResult.metrics
    for metricName in self.__metricNames:
      outputRow.append(metrics.get(metricName, 0.0))

    #print "DEBUG: _BasicPredictionWriter: writing outputRow: %r" % (outputRow,)

    self.__dataset.appendRecord(outputRow)

    self.__dataset.flush()

    return