def getClosest(self, inputPattern, topKCategories=3):
    """Returns the index of the pattern that is closest to inputPattern,
    the distances of all patterns to inputPattern, and the indices of the k
    closest categories.
    """
    inferenceResult = numpy.zeros(max(self._categoryList)+1)
    dist = self._getDistances(inputPattern)

    sorted = dist.argsort()

    validVectorCount = len(self._categoryList) - self._categoryList.count(-1)
    for j in sorted[:min(self.k, validVectorCount)]:
      inferenceResult[self._categoryList[j]] += 1.0

    winner = inferenceResult.argmax()

    topNCats = []
    for i in range(topKCategories):
      topNCats.append((self._categoryList[sorted[i]], dist[sorted[i]] ))

    return winner, dist, topNCats