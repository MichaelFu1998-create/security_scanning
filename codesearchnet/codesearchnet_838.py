def compute(self, inputs, outputs):
    """
    Process one input sample.
    This method is called by the runtime engine.

    :param inputs: (dict) mapping region input names to numpy.array values
    :param outputs: (dict) mapping region output names to numpy.arrays that 
           should be populated with output values by this method
    """

    # This flag helps to prevent double-computation, in case the deprecated
    # customCompute() method is being called in addition to compute() called
    # when network.run() is called
    self._computeFlag = True

    patternNZ = inputs["bottomUpIn"].nonzero()[0]

    if self.learningMode:
      # An input can potentially belong to multiple categories.
      # If a category value is < 0, it means that the input does not belong to
      # that category.
      categories = [category for category in inputs["categoryIn"]
                    if category >= 0]

      if len(categories) > 0:
        # Allow to train on multiple input categories.
        bucketIdxList = []
        actValueList = []
        for category in categories:
          bucketIdxList.append(int(category))
          if "actValueIn" not in inputs:
            actValueList.append(int(category))
          else:
            actValueList.append(float(inputs["actValueIn"]))

        classificationIn = {"bucketIdx": bucketIdxList,
                            "actValue": actValueList}
      else:
        # If the input does not belong to a category, i.e. len(categories) == 0,
        # then look for bucketIdx and actValueIn.
        if "bucketIdxIn" not in inputs:
          raise KeyError("Network link missing: bucketIdxOut -> bucketIdxIn")
        if "actValueIn" not in inputs:
          raise KeyError("Network link missing: actValueOut -> actValueIn")

        classificationIn = {"bucketIdx": int(inputs["bucketIdxIn"]),
                            "actValue": float(inputs["actValueIn"])}
    else:
      # Use Dummy classification input, because this param is required even for
      # inference mode. Because learning is off, the classifier is not learning
      # this dummy input. Inference only here.
      classificationIn = {"actValue": 0, "bucketIdx": 0}

    # Perform inference if self.inferenceMode is True
    # Train classifier if self.learningMode is True
    clResults = self._sdrClassifier.compute(recordNum=self.recordNum,
                                            patternNZ=patternNZ,
                                            classification=classificationIn,
                                            learn=self.learningMode,
                                            infer=self.inferenceMode)

    # fill outputs with clResults
    if clResults is not None and len(clResults) > 0:
      outputs['actualValues'][:len(clResults["actualValues"])] = \
        clResults["actualValues"]

      for step in self.stepsList:
        stepIndex = self.stepsList.index(step)
        categoryOut = clResults["actualValues"][clResults[step].argmax()]
        outputs['categoriesOut'][stepIndex] = categoryOut

        # Flatten the rest of the output. For example:
        #   Original dict  {1 : [0.1, 0.3, 0.2, 0.7]
        #                   4 : [0.2, 0.4, 0.3, 0.5]}
        #   becomes: [0.1, 0.3, 0.2, 0.7, 0.2, 0.4, 0.3, 0.5]
        stepProbabilities = clResults[step]
        for categoryIndex in xrange(self.maxCategoryCount):
          flatIndex = categoryIndex + stepIndex * self.maxCategoryCount
          if categoryIndex < len(stepProbabilities):
            outputs['probabilities'][flatIndex] = \
              stepProbabilities[categoryIndex]
          else:
            outputs['probabilities'][flatIndex] = 0.0

    self.recordNum += 1