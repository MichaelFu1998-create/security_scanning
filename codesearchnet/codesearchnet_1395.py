def learn(self, inputPattern, inputCategory, partitionId=None, isSparse=0,
            rowID=None):
    """
    Train the classifier to associate specified input pattern with a
    particular category.

    :param inputPattern: (list) The pattern to be assigned a category. If
        isSparse is 0, this should be a dense array (both ON and OFF bits
        present). Otherwise, if isSparse > 0, this should be a list of the
        indices of the non-zero bits in sorted order

    :param inputCategory: (int) The category to be associated to the training
        pattern

    :param partitionId: (int) partitionID allows you to associate an id with each
        input vector. It can be used to associate input patterns stored in the
        classifier with an external id. This can be useful for debugging or
        visualizing. Another use case is to ignore vectors with a specific id
        during inference (see description of infer() for details). There can be
        at most one partitionId per stored pattern (i.e. if two patterns are
        within distThreshold, only the first partitionId will be stored). This
        is an optional parameter.

    :param isSparse: (int) 0 if the input pattern is a dense representation.
        When the input pattern is a list of non-zero indices, then isSparse
        is the number of total bits (n). E.g. for the dense array
        [0, 1, 1, 0, 0, 1], isSparse should be `0`. For the equivalent sparse
        representation [1, 2, 5] (which specifies the indices of active bits),
        isSparse should be `6`, which is the total number of bits in the input
        space.

    :param rowID: (int) UNKNOWN

    :returns: The number of patterns currently stored in the classifier
    """
    if self.verbosity >= 1:
      print "%s learn:" % g_debugPrefix
      print "  category:", int(inputCategory)
      print "  active inputs:", _labeledInput(inputPattern,
                                              cellsPerCol=self.cellsPerCol)

    if isSparse > 0:
      assert all(inputPattern[i] <= inputPattern[i+1]
                 for i in xrange(len(inputPattern)-1)), \
                     "Sparse inputPattern must be sorted."
      assert all(bit < isSparse for bit in inputPattern), \
        ("Sparse inputPattern must not index outside the dense "
         "representation's bounds.")

    if rowID is None:
      rowID = self._iterationIdx

    # Dense vectors
    if not self.useSparseMemory:

      # Not supported
      assert self.cellsPerCol == 0, "not implemented for dense vectors"

      # If the input was given in sparse form, convert it to dense
      if isSparse > 0:
        denseInput = numpy.zeros(isSparse)
        denseInput[inputPattern] = 1.0
        inputPattern = denseInput

      if self._specificIndexTraining and not self._nextTrainingIndices:
        # Specific index mode without any index provided - skip training
        return self._numPatterns

      if self._Memory is None:
        # Initialize memory with 100 rows and numPatterns = 0
        inputWidth = len(inputPattern)
        self._Memory = numpy.zeros((100,inputWidth))
        self._numPatterns = 0
        self._M = self._Memory[:self._numPatterns]

      addRow = True

      if self._vt is not None:
        # Compute projection
        inputPattern = numpy.dot(self._vt, inputPattern - self._mean)

      if self.distThreshold > 0:
        # Check if input is too close to an existing input to be accepted
        dist = self._calcDistance(inputPattern)
        minDist = dist.min()
        addRow = (minDist >= self.distThreshold)

      if addRow:
        self._protoSizes = None     # need to re-compute
        if self._numPatterns == self._Memory.shape[0]:
          # Double the size of the memory
          self._doubleMemoryNumRows()

        if not self._specificIndexTraining:
          # Normal learning - append the new input vector
          self._Memory[self._numPatterns] = inputPattern
          self._numPatterns += 1
          self._categoryList.append(int(inputCategory))
        else:
          # Specific index training mode - insert vector in specified slot
          vectorIndex = self._nextTrainingIndices.pop(0)
          while vectorIndex >= self._Memory.shape[0]:
            self._doubleMemoryNumRows()
          self._Memory[vectorIndex] = inputPattern
          self._numPatterns = max(self._numPatterns, vectorIndex + 1)
          if vectorIndex >= len(self._categoryList):
            self._categoryList += [-1] * (vectorIndex -
                                          len(self._categoryList) + 1)
          self._categoryList[vectorIndex] = int(inputCategory)

        # Set _M to the "active" part of _Memory
        self._M = self._Memory[0:self._numPatterns]

        self._addPartitionId(self._numPatterns-1, partitionId)

    # Sparse vectors
    else:

      # If the input was given in sparse form, convert it to dense if necessary
      if isSparse > 0 and (self._vt is not None or self.distThreshold > 0 \
              or self.numSVDDims is not None or self.numSVDSamples > 0 \
              or self.numWinners > 0):
          denseInput = numpy.zeros(isSparse)
          denseInput[inputPattern] = 1.0
          inputPattern = denseInput
          isSparse = 0

      # Get the input width
      if isSparse > 0:
        inputWidth = isSparse
      else:
        inputWidth = len(inputPattern)

      # Allocate storage if this is the first training vector
      if self._Memory is None:
        self._Memory = NearestNeighbor(0, inputWidth)

      # Support SVD if it is on
      if self._vt is not None:
        inputPattern = numpy.dot(self._vt, inputPattern - self._mean)

      # Threshold the input, zeroing out entries that are too close to 0.
      #  This is only done if we are given a dense input.
      if isSparse == 0:
        thresholdedInput = self._sparsifyVector(inputPattern, True)
      addRow = True

      # If given the layout of the cells, then turn on the logic that stores
      # only the start cell for bursting columns.
      if self.cellsPerCol >= 1:
        burstingCols = thresholdedInput.reshape(-1,
                                  self.cellsPerCol).min(axis=1).nonzero()[0]
        for col in burstingCols:
          thresholdedInput[(col * self.cellsPerCol) + 1 :
                           (col * self.cellsPerCol) + self.cellsPerCol] = 0


      # Don't learn entries that are too close to existing entries.
      if self._Memory.nRows() > 0:
        dist = None
        # if this vector is a perfect match for one we already learned, then
        #  replace the category - it may have changed with online learning on.
        if self.replaceDuplicates:
          dist = self._calcDistance(thresholdedInput, distanceNorm=1)
          if dist.min() == 0:
            rowIdx = dist.argmin()
            self._categoryList[rowIdx] = int(inputCategory)
            if self.fixedCapacity:
              self._categoryRecencyList[rowIdx] = rowID
            addRow = False

        # Don't add this vector if it matches closely with another we already
        #  added
        if self.distThreshold > 0:
          if dist is None or self.distanceNorm != 1:
            dist = self._calcDistance(thresholdedInput)
          minDist = dist.min()
          addRow = (minDist >= self.distThreshold)
          if not addRow:
            if self.fixedCapacity:
              rowIdx = dist.argmin()
              self._categoryRecencyList[rowIdx] = rowID


      # If sparsity is too low, we do not want to add this vector
      if addRow and self.minSparsity > 0.0:
        if isSparse==0:
          sparsity = ( float(len(thresholdedInput.nonzero()[0])) /
                       len(thresholdedInput) )
        else:
          sparsity = float(len(inputPattern)) / isSparse
        if sparsity < self.minSparsity:
          addRow = False

      # Add the new sparse vector to our storage
      if addRow:
        self._protoSizes = None     # need to re-compute
        if isSparse == 0:
          self._Memory.addRow(thresholdedInput)
        else:
          self._Memory.addRowNZ(inputPattern, [1]*len(inputPattern))
        self._numPatterns += 1
        self._categoryList.append(int(inputCategory))
        self._addPartitionId(self._numPatterns-1, partitionId)
        if self.fixedCapacity:
          self._categoryRecencyList.append(rowID)
          if self._numPatterns > self.maxStoredPatterns and \
            self.maxStoredPatterns > 0:
            leastRecentlyUsedPattern = numpy.argmin(self._categoryRecencyList)
            self._Memory.deleteRow(leastRecentlyUsedPattern)
            self._categoryList.pop(leastRecentlyUsedPattern)
            self._categoryRecencyList.pop(leastRecentlyUsedPattern)
            self._numPatterns -= 1

    if self.numSVDDims is not None and self.numSVDSamples > 0 \
          and self._numPatterns == self.numSVDSamples:
        self.computeSVD()

    return self._numPatterns