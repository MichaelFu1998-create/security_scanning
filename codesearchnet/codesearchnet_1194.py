def _handleSDRClassifierMultiStep(self, patternNZ,
                                    inputTSRecordIdx,
                                    rawInput):
    """ Handle the CLA Classifier compute logic when implementing multi-step
    prediction. This is where the patternNZ is associated with one of the
    other fields from the dataset 0 to N steps in the future. This method is
    used by each type of network (encoder only, SP only, SP +TM) to handle the
    compute logic through the CLA Classifier. It fills in the inference dict with
    the results of the compute.

    Parameters:
    -------------------------------------------------------------------
    patternNZ: The input to the CLA Classifier as a list of active input indices
    inputTSRecordIdx: The index of the record as computed from the timestamp
                  and aggregation interval. This normally increments by 1
                  each time unless there are missing records. If there is no
                  aggregation interval or timestamp in the data, this will be
                  None.
    rawInput:   The raw input to the sensor, as a dict.
    """
    inferenceArgs = self.getInferenceArgs()
    predictedFieldName = inferenceArgs.get('predictedField', None)
    if predictedFieldName is None:
      raise ValueError(
        "No predicted field was enabled! Did you call enableInference()?"
      )
    self._predictedFieldName = predictedFieldName

    classifier = self._getClassifierRegion()
    if not self._hasCL or classifier is None:
      # No classifier so return an empty dict for inferences.
      return {}

    sensor = self._getSensorRegion()
    minLikelihoodThreshold = self._minLikelihoodThreshold
    maxPredictionsPerStep = self._maxPredictionsPerStep
    needLearning = self.isLearningEnabled()
    inferences = {}

    # Get the classifier input encoder, if we don't have it already
    if self._classifierInputEncoder is None:
      if predictedFieldName is None:
        raise RuntimeError("This experiment description is missing "
              "the 'predictedField' in its config, which is required "
              "for multi-step prediction inference.")

      encoderList = sensor.getSelf().encoder.getEncoderList()
      self._numFields = len(encoderList)

      # This is getting index of predicted field if being fed to CLA.
      fieldNames = sensor.getSelf().encoder.getScalarNames()
      if predictedFieldName in fieldNames:
        self._predictedFieldIdx = fieldNames.index(predictedFieldName)
      else:
        # Predicted field was not fed into the network, only to the classifier
        self._predictedFieldIdx = None

      # In a multi-step model, the classifier input encoder is separate from
      #  the other encoders and always disabled from going into the bottom of
      # the network.
      if sensor.getSelf().disabledEncoder is not None:
        encoderList = sensor.getSelf().disabledEncoder.getEncoderList()
      else:
        encoderList = []
      if len(encoderList) >= 1:
        fieldNames = sensor.getSelf().disabledEncoder.getScalarNames()
        self._classifierInputEncoder = encoderList[fieldNames.index(
                                                        predictedFieldName)]
      else:
        # Legacy multi-step networks don't have a separate encoder for the
        #  classifier, so use the one that goes into the bottom of the network
        encoderList = sensor.getSelf().encoder.getEncoderList()
        self._classifierInputEncoder = encoderList[self._predictedFieldIdx]



    # Get the actual value and the bucket index for this sample. The
    # predicted field may not be enabled for input to the network, so we
    # explicitly encode it outside of the sensor
    # TODO: All this logic could be simpler if in the encoder itself
    if not predictedFieldName in rawInput:
      raise ValueError("Input row does not contain a value for the predicted "
                       "field configured for this model. Missing value for '%s'"
                       % predictedFieldName)
    absoluteValue = rawInput[predictedFieldName]
    bucketIdx = self._classifierInputEncoder.getBucketIndices(absoluteValue)[0]

    # Convert the absolute values to deltas if necessary
    # The bucket index should be handled correctly by the underlying delta encoder
    if isinstance(self._classifierInputEncoder, DeltaEncoder):
      # Make the delta before any values have been seen 0 so that we do not mess up the
      # range for the adaptive scalar encoder.
      if not hasattr(self,"_ms_prevVal"):
        self._ms_prevVal = absoluteValue
      prevValue = self._ms_prevVal
      self._ms_prevVal = absoluteValue
      actualValue = absoluteValue - prevValue
    else:
      actualValue = absoluteValue

    if isinstance(actualValue, float) and math.isnan(actualValue):
      actualValue = SENTINEL_VALUE_FOR_MISSING_DATA


    # Pass this information to the classifier's custom compute method
    # so that it can assign the current classification to possibly
    # multiple patterns from the past and current, and also provide
    # the expected classification for some time step(s) in the future.
    classifier.setParameter('inferenceMode', True)
    classifier.setParameter('learningMode', needLearning)
    classificationIn = {'bucketIdx': bucketIdx,
                        'actValue': actualValue}

    # Handle missing records
    if inputTSRecordIdx is not None:
      recordNum = inputTSRecordIdx
    else:
      recordNum = self.__numRunCalls
    clResults = classifier.getSelf().customCompute(recordNum=recordNum,
                                           patternNZ=patternNZ,
                                           classification=classificationIn)

    # ---------------------------------------------------------------
    # Get the prediction for every step ahead learned by the classifier
    predictionSteps = classifier.getParameter('steps')
    predictionSteps = [int(x) for x in predictionSteps.split(',')]

    # We will return the results in this dict. The top level keys
    # are the step number, the values are the relative likelihoods for
    # each classification value in that time step, represented as
    # another dict where the keys are the classification values and
    # the values are the relative likelihoods.
    inferences[InferenceElement.multiStepPredictions] = dict()
    inferences[InferenceElement.multiStepBestPredictions] = dict()
    inferences[InferenceElement.multiStepBucketLikelihoods] = dict()


    # ======================================================================
    # Plug in the predictions for each requested time step.
    for steps in predictionSteps:
      # From the clResults, compute the predicted actual value. The
      # SDRClassifier classifies the bucket index and returns a list of
      # relative likelihoods for each bucket. Let's find the max one
      # and then look up the actual value from that bucket index
      likelihoodsVec = clResults[steps]
      bucketValues = clResults['actualValues']

      # Create a dict of value:likelihood pairs. We can't simply use
      #  dict(zip(bucketValues, likelihoodsVec)) because there might be
      #  duplicate bucketValues (this happens early on in the model when
      #  it doesn't have actual values for each bucket so it returns
      #  multiple buckets with the same default actual value).
      likelihoodsDict = dict()
      bestActValue = None
      bestProb = None
      for (actValue, prob) in zip(bucketValues, likelihoodsVec):
        if actValue in likelihoodsDict:
          likelihoodsDict[actValue] += prob
        else:
          likelihoodsDict[actValue] = prob
        # Keep track of best
        if bestProb is None or likelihoodsDict[actValue] > bestProb:
          bestProb = likelihoodsDict[actValue]
          bestActValue = actValue


      # Remove entries with 0 likelihood or likelihood less than
      # minLikelihoodThreshold, but don't leave an empty dict.
      likelihoodsDict = HTMPredictionModel._removeUnlikelyPredictions(
          likelihoodsDict, minLikelihoodThreshold, maxPredictionsPerStep)

      # calculate likelihood for each bucket
      bucketLikelihood = {}
      for k in likelihoodsDict.keys():
        bucketLikelihood[self._classifierInputEncoder.getBucketIndices(k)[0]] = (
                                                                likelihoodsDict[k])

      # ---------------------------------------------------------------------
      # If we have a delta encoder, we have to shift our predicted output value
      #  by the sum of the deltas
      if isinstance(self._classifierInputEncoder, DeltaEncoder):
        # Get the prediction history for this number of timesteps.
        # The prediction history is a store of the previous best predicted values.
        # This is used to get the final shift from the current absolute value.
        if not hasattr(self, '_ms_predHistories'):
          self._ms_predHistories = dict()
        predHistories = self._ms_predHistories
        if not steps in predHistories:
          predHistories[steps] = deque()
        predHistory = predHistories[steps]

        # Find the sum of the deltas for the steps and use this to generate
        # an offset from the current absolute value
        sumDelta = sum(predHistory)
        offsetDict = dict()
        for (k, v) in likelihoodsDict.iteritems():
          if k is not None:
            # Reconstruct the absolute value based on the current actual value,
            # the best predicted values from the previous iterations,
            # and the current predicted delta
            offsetDict[absoluteValue+float(k)+sumDelta] = v

        # calculate likelihood for each bucket
        bucketLikelihoodOffset = {}
        for k in offsetDict.keys():
          bucketLikelihoodOffset[self._classifierInputEncoder.getBucketIndices(k)[0]] = (
                                                                            offsetDict[k])


        # Push the current best delta to the history buffer for reconstructing the final delta
        if bestActValue is not None:
          predHistory.append(bestActValue)
        # If we don't need any more values in the predictionHistory, pop off
        # the earliest one.
        if len(predHistory) >= steps:
          predHistory.popleft()

        # Provide the offsetDict as the return value
        if len(offsetDict)>0:
          inferences[InferenceElement.multiStepPredictions][steps] = offsetDict
          inferences[InferenceElement.multiStepBucketLikelihoods][steps] = bucketLikelihoodOffset
        else:
          inferences[InferenceElement.multiStepPredictions][steps] = likelihoodsDict
          inferences[InferenceElement.multiStepBucketLikelihoods][steps] = bucketLikelihood

        if bestActValue is None:
          inferences[InferenceElement.multiStepBestPredictions][steps] = None
        else:
          inferences[InferenceElement.multiStepBestPredictions][steps] = (
            absoluteValue + sumDelta + bestActValue)

      # ---------------------------------------------------------------------
      # Normal case, no delta encoder. Just plug in all our multi-step predictions
      #  with likelihoods as well as our best prediction
      else:
        # The multiStepPredictions element holds the probabilities for each
        #  bucket
        inferences[InferenceElement.multiStepPredictions][steps] = (
                                                      likelihoodsDict)
        inferences[InferenceElement.multiStepBestPredictions][steps] = (
                                                      bestActValue)
        inferences[InferenceElement.multiStepBucketLikelihoods][steps] = (
                                                      bucketLikelihood)


    return inferences