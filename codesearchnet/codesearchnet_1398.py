def infer(self, inputPattern, computeScores=True, overCategories=True,
            partitionId=None):
    """Finds the category that best matches the input pattern. Returns the
    winning category index as well as a distribution over all categories.

    :param inputPattern: (list or array) The pattern to be classified. This
        must be a dense representation of the array (e.g. [0, 0, 1, 1, 0, 1]).

    :param computeScores: NO EFFECT

    :param overCategories: NO EFFECT

    :param partitionId: (int) If provided, all training vectors with partitionId
        equal to that of the input pattern are ignored.
        For example, this may be used to perform k-fold cross validation
        without repopulating the classifier. First partition all the data into
        k equal partitions numbered 0, 1, 2, ... and then call learn() for each
        vector passing in its partitionId. Then, during inference, by passing
        in the partition ID in the call to infer(), all other vectors with the
        same partitionId are ignored simulating the effect of repopulating the
        classifier while ommitting the training vectors in the same partition.

    :returns: 4-tuple with these keys:

      - ``winner``: The category with the greatest number of nearest neighbors
          within the kth nearest neighbors. If the inferenceResult contains no
          neighbors, the value of winner is None. This can happen, for example,
          in cases of exact matching, if there are no stored vectors, or if
          minSparsity is not met.
      - ``inferenceResult``: A list of length numCategories, each entry contains
          the number of neighbors within the top k neighbors that are in that
          category.
      - ``dist``: A list of length numPrototypes. Each entry is the distance
          from the unknown to that prototype. All distances are between 0.0 and
          1.0.
      - ``categoryDist``: A list of length numCategories. Each entry is the
                        distance from the unknown to the nearest prototype of
                        that category. All distances are between 0 and 1.0.
    """

    # Calculate sparsity. If sparsity is too low, we do not want to run
    # inference with this vector
    sparsity = 0.0
    if self.minSparsity > 0.0:
      sparsity = ( float(len(inputPattern.nonzero()[0])) /
                   len(inputPattern) )

    if len(self._categoryList) == 0 or sparsity < self.minSparsity:
      # No categories learned yet; i.e. first inference w/ online learning or
      # insufficient sparsity
      winner = None
      inferenceResult = numpy.zeros(1)
      dist = numpy.ones(1)
      categoryDist = numpy.ones(1)

    else:
      maxCategoryIdx = max(self._categoryList)
      inferenceResult = numpy.zeros(maxCategoryIdx+1)
      dist = self._getDistances(inputPattern, partitionId=partitionId)
      validVectorCount = len(self._categoryList) - self._categoryList.count(-1)

      # Loop through the indices of the nearest neighbors.
      if self.exact:
        # Is there an exact match in the distances?
        exactMatches = numpy.where(dist<0.00001)[0]
        if len(exactMatches) > 0:
          for i in exactMatches[:min(self.k, validVectorCount)]:
            inferenceResult[self._categoryList[i]] += 1.0
      else:
        sorted = dist.argsort()
        for j in sorted[:min(self.k, validVectorCount)]:
          inferenceResult[self._categoryList[j]] += 1.0

      # Prepare inference results.
      if inferenceResult.any():
        winner = inferenceResult.argmax()
        inferenceResult /= inferenceResult.sum()
      else:
        winner = None
      categoryDist = min_score_per_category(maxCategoryIdx,
                                            self._categoryList, dist)
      categoryDist.clip(0, 1.0, categoryDist)

    if self.verbosity >= 1:
      print "%s infer:" % (g_debugPrefix)
      print "  active inputs:",  _labeledInput(inputPattern,
                                               cellsPerCol=self.cellsPerCol)
      print "  winner category:", winner
      print "  pct neighbors of each category:", inferenceResult
      print "  dist of each prototype:", dist
      print "  dist of each category:", categoryDist

    result = (winner, inferenceResult, dist, categoryDist)
    return result