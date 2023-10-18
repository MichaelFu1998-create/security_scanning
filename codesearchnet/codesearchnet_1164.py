def compute(self, recordNum, patternNZ, classification, learn, infer):
    """
    Process one input sample.

    This method is called by outer loop code outside the nupic-engine. We
    use this instead of the nupic engine compute() because our inputs and
    outputs aren't fixed size vectors of reals.


    :param recordNum: Record number of this input pattern. Record numbers
      normally increase sequentially by 1 each time unless there are missing
      records in the dataset. Knowing this information insures that we don't get
      confused by missing records.

    :param patternNZ: List of the active indices from the output below. When the
      input is from TemporalMemory, this list should be the indices of the
      active cells.

    :param classification: Dict of the classification information where:

      - bucketIdx: list of indices of the encoder bucket
      - actValue: list of actual values going into the encoder

      Classification could be None for inference mode.
    :param learn: (bool) if true, learn this sample
    :param infer: (bool) if true, perform inference

    :return:    Dict containing inference results, there is one entry for each
                step in self.steps, where the key is the number of steps, and
                the value is an array containing the relative likelihood for
                each bucketIdx starting from bucketIdx 0.

                There is also an entry containing the average actual value to
                use for each bucket. The key is 'actualValues'.

                for example:

                .. code-block:: python

                   {1 :             [0.1, 0.3, 0.2, 0.7],
                     4 :             [0.2, 0.4, 0.3, 0.5],
                     'actualValues': [1.5, 3,5, 5,5, 7.6],
                   }
    """
    if self.verbosity >= 1:
      print "  learn:", learn
      print "  recordNum:", recordNum
      print "  patternNZ (%d):" % len(patternNZ), patternNZ
      print "  classificationIn:", classification

    # ensures that recordNum increases monotonically
    if len(self._patternNZHistory) > 0:
      if recordNum < self._patternNZHistory[-1][0]:
        raise ValueError("the record number has to increase monotonically")

    # Store pattern in our history if this is a new record
    if len(self._patternNZHistory) == 0 or \
                    recordNum > self._patternNZHistory[-1][0]:
      self._patternNZHistory.append((recordNum, patternNZ))

    # To allow multi-class classification, we need to be able to run learning
    # without inference being on. So initialize retval outside
    # of the inference block.
    retval = {}

    # Update maxInputIdx and augment weight matrix with zero padding
    if max(patternNZ) > self._maxInputIdx:
      newMaxInputIdx = max(patternNZ)
      for nSteps in self.steps:
        self._weightMatrix[nSteps] = numpy.concatenate((
          self._weightMatrix[nSteps],
          numpy.zeros(shape=(newMaxInputIdx-self._maxInputIdx,
                             self._maxBucketIdx+1))), axis=0)
      self._maxInputIdx = int(newMaxInputIdx)

    # Get classification info
    if classification is not None:
      if type(classification["bucketIdx"]) is not list:
        bucketIdxList = [classification["bucketIdx"]]
        actValueList = [classification["actValue"]]
        numCategory = 1
      else:
        bucketIdxList = classification["bucketIdx"]
        actValueList = classification["actValue"]
        numCategory = len(classification["bucketIdx"])
    else:
      if learn:
        raise ValueError("classification cannot be None when learn=True")
      actValueList = None
      bucketIdxList = None
    # ------------------------------------------------------------------------
    # Inference:
    # For each active bit in the activationPattern, get the classification
    # votes
    if infer:
      retval = self.infer(patternNZ, actValueList)


    if learn and classification["bucketIdx"] is not None:
      for categoryI in range(numCategory):
        bucketIdx = bucketIdxList[categoryI]
        actValue = actValueList[categoryI]

        # Update maxBucketIndex and augment weight matrix with zero padding
        if bucketIdx > self._maxBucketIdx:
          for nSteps in self.steps:
            self._weightMatrix[nSteps] = numpy.concatenate((
              self._weightMatrix[nSteps],
              numpy.zeros(shape=(self._maxInputIdx+1,
                                 bucketIdx-self._maxBucketIdx))), axis=1)

          self._maxBucketIdx = int(bucketIdx)

        # Update rolling average of actual values if it's a scalar. If it's
        # not, it must be a category, in which case each bucket only ever
        # sees one category so we don't need a running average.
        while self._maxBucketIdx > len(self._actualValues) - 1:
          self._actualValues.append(None)
        if self._actualValues[bucketIdx] is None:
          self._actualValues[bucketIdx] = actValue
        else:
          if (isinstance(actValue, int) or
                isinstance(actValue, float) or
                isinstance(actValue, long)):
            self._actualValues[bucketIdx] = ((1.0 - self.actValueAlpha)
                                             * self._actualValues[bucketIdx]
                                             + self.actValueAlpha * actValue)
          else:
            self._actualValues[bucketIdx] = actValue

      for (learnRecordNum, learnPatternNZ) in self._patternNZHistory:
        error = self._calculateError(recordNum, bucketIdxList)

        nSteps = recordNum - learnRecordNum
        if nSteps in self.steps:
          for bit in learnPatternNZ:
            self._weightMatrix[nSteps][bit, :] += self.alpha * error[nSteps]

    # ------------------------------------------------------------------------
    # Verbose print
    if infer and self.verbosity >= 1:
      print "  inference: combined bucket likelihoods:"
      print "    actual bucket values:", retval["actualValues"]
      for (nSteps, votes) in retval.items():
        if nSteps == "actualValues":
          continue
        print "    %d steps: " % (nSteps), _pFormatArray(votes)
        bestBucketIdx = votes.argmax()
        print ("      most likely bucket idx: "
               "%d, value: %s" % (bestBucketIdx,
                                  retval["actualValues"][bestBucketIdx]))
      print

    return retval