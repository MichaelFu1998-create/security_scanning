def compute(self, inputs, outputs):
    """
    Process one input sample. This method is called by the runtime engine.

    .. note:: the number of input categories may vary, but the array size is 
       fixed to the max number of categories allowed (by a lower region), so 
       "unused" indices of the input category array are filled with -1s.

    TODO: confusion matrix does not support multi-label classification

    :param inputs: (dict) mapping region input names to numpy.array values
    :param outputs: (dict) mapping region output names to numpy.arrays that 
           should be populated with output values by this method
    """

    #raise Exception('MULTI-LINE DUMMY\nMULTI-LINE DUMMY')
    #For backward compatibility
    if self._useAuxiliary is None:
      self._useAuxiliary = False

    # If the first time being called, then print potential warning messsages
    if self._firstComputeCall:
      self._firstComputeCall = False
      if self._useAuxiliary:
        #print "\n  Auxiliary input stream from Image Sensor enabled."
        if self._justUseAuxiliary == True:
          print "  Warning: You have chosen to ignore the image data and instead just use the auxiliary data stream."


    # Format inputs
    #childInputs = [x.wvector(0) for x in inputs["bottomUpIn"]]
    #inputVector = numpy.concatenate([x.array() for x in childInputs])
    inputVector = inputs['bottomUpIn']

    # Look for auxiliary input
    if self._useAuxiliary==True:
      #auxVector = inputs['auxDataIn'][0].wvector(0).array()
      auxVector = inputs['auxDataIn']
      if auxVector.dtype != numpy.float32:
        raise RuntimeError, "KNNClassifierRegion expects numpy.float32 for the auxiliary data vector"
      if self._justUseAuxiliary == True:
        #inputVector = inputs['auxDataIn'][0].wvector(0).array()
        inputVector = inputs['auxDataIn']
      else:
        #inputVector = numpy.concatenate([inputVector, inputs['auxDataIn'][0].wvector(0).array()])
        inputVector = numpy.concatenate([inputVector, inputs['auxDataIn']])

    # Logging
    #self.handleLogInput(childInputs)
    self.handleLogInput([inputVector])

    # Read the category.
    assert "categoryIn" in inputs, "No linked category input."
    categories = inputs['categoryIn']

    # Read the partition ID.
    if "partitionIn" in inputs:
      assert len(inputs["partitionIn"]) == 1, "Must have exactly one link to partition input."
      partInput = inputs['partitionIn']
      assert len(partInput) == 1, "Partition input element count must be exactly 1."
      partition = int(partInput[0])
    else:
      partition = None


    # ---------------------------------------------------------------------
    # Inference (can be done simultaneously with learning)
    if self.inferenceMode:
      categoriesOut = outputs['categoriesOut']
      probabilitiesOut = outputs['categoryProbabilitiesOut']

      # If we are sphering, then apply normalization
      if self._doSphering:
        inputVector = (inputVector + self._normOffset) * self._normScale

      nPrototypes = 0
      if "bestPrototypeIndices" in outputs:
        #bestPrototypeIndicesOut = outputs["bestPrototypeIndices"].wvector()
        bestPrototypeIndicesOut = outputs["bestPrototypeIndices"]
        nPrototypes = len(bestPrototypeIndicesOut)

      winner, inference, protoScores, categoryDistances = \
                  self._knn.infer(inputVector, partitionId=partition)



      if not self.keepAllDistances:
        self._protoScores = protoScores
      else:
        # Keep all prototype scores in an array
        if self._protoScores is None:
          self._protoScores = numpy.zeros((1, protoScores.shape[0]),
                                          protoScores.dtype)
          self._protoScores[0,:] = protoScores#.reshape(1, protoScores.shape[0])
          self._protoScoreCount = 1
        else:
          if self._protoScoreCount == self._protoScores.shape[0]:
            # Double the size of the array
            newProtoScores = numpy.zeros((self._protoScores.shape[0] * 2,
                                          self._protoScores.shape[1]),
                                          self._protoScores.dtype)
            newProtoScores[:self._protoScores.shape[0],:] = self._protoScores
            self._protoScores = newProtoScores
          # Store the new prototype score
          self._protoScores[self._protoScoreCount,:] = protoScores
          self._protoScoreCount += 1
      self._categoryDistances = categoryDistances


      # --------------------------------------------------------------------
      # Compute the probability of each category
      if self.outputProbabilitiesByDist:
        scores = 1.0 - self._categoryDistances
      else:
        scores = inference

      # Probability is simply the scores/scores.sum()
      total = scores.sum()
      if total == 0:
        numScores = len(scores)
        probabilities = numpy.ones(numScores) / numScores
      else:
        probabilities = scores / total


      # -------------------------------------------------------------------
      # Fill the output vectors with our results
      nout = min(len(categoriesOut), len(inference))
      categoriesOut.fill(0)
      categoriesOut[0:nout] = inference[0:nout]

      probabilitiesOut.fill(0)
      probabilitiesOut[0:nout] = probabilities[0:nout]

      if self.verbosity >= 1:
        print "KNNRegion: categoriesOut: ", categoriesOut[0:nout]
        print "KNNRegion: probabilitiesOut: ", probabilitiesOut[0:nout]

      if self._scanInfo is not None:
        self._scanResults = [tuple(inference[:nout])]

      # Update the stored confusion matrix.
      for category in categories:
        if category >= 0:
          dims = max(int(category)+1, len(inference))
          oldDims = len(self.confusion)
          if oldDims < dims:
            confusion = numpy.zeros((dims, dims))
            confusion[0:oldDims, 0:oldDims] = self.confusion
            self.confusion = confusion
          self.confusion[inference.argmax(), int(category)] += 1

      # Calculate the best prototype indices
      if nPrototypes > 1:
        bestPrototypeIndicesOut.fill(0)
        if categoryDistances is not None:
          indices = categoryDistances.argsort()
          nout = min(len(indices), nPrototypes)
          bestPrototypeIndicesOut[0:nout] = indices[0:nout]
      elif nPrototypes == 1:
        if (categoryDistances is not None) and len(categoryDistances):
          bestPrototypeIndicesOut[0] = categoryDistances.argmin()
        else:
          bestPrototypeIndicesOut[0] = 0

      # Logging
      self.handleLogOutput(inference)

    # ---------------------------------------------------------------------
    # Learning mode
    if self.learningMode:
      if (self.acceptanceProbability < 1.0) and \
            (self._rgen.getReal64() > self.acceptanceProbability):
        pass

      else:
        # Accept the input
        for category in categories:
          if category >= 0:
            # category values of -1 are to be skipped (they are non-categories)
            if self._doSphering:
              # If we are sphering, then we can't provide the data to the KNN
              # library until we have computed per-dimension normalization
              # constants. So instead, we'll just store each training sample.
              self._storeSample(inputVector, category, partition)
            else:
              # Pass the raw training sample directly to the KNN library.
              self._knn.learn(inputVector, category, partition)

    self._epoch += 1