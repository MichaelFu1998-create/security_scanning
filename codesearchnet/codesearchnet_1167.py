def _calculateError(self, recordNum, bucketIdxList):
    """
    Calculate error signal

    :param bucketIdxList: list of encoder buckets

    :return: dict containing error. The key is the number of steps
             The value is a numpy array of error at the output layer
    """
    error = dict()
    targetDist = numpy.zeros(self._maxBucketIdx + 1)
    numCategories = len(bucketIdxList)
    for bucketIdx in bucketIdxList:
      targetDist[bucketIdx] = 1.0/numCategories

    for (learnRecordNum, learnPatternNZ) in self._patternNZHistory:
      nSteps = recordNum - learnRecordNum
      if nSteps in self.steps:
        predictDist = self.inferSingleStep(learnPatternNZ,
                                           self._weightMatrix[nSteps])
        error[nSteps] = targetDist - predictDist

    return error