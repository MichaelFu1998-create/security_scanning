def _calcDistance(self, inputPattern, distanceNorm=None):
    """Calculate the distances from inputPattern to all stored patterns. All
    distances are between 0.0 and 1.0

    :param inputPattern The pattern from which distances to all other patterns
        are calculated

    :param distanceNorm Degree of the distance norm
    """
    if distanceNorm is None:
      distanceNorm = self.distanceNorm

    # Sparse memory
    if self.useSparseMemory:
      if self._protoSizes is None:
        self._protoSizes = self._Memory.rowSums()
      overlapsWithProtos = self._Memory.rightVecSumAtNZ(inputPattern)
      inputPatternSum = inputPattern.sum()

      if self.distanceMethod == "rawOverlap":
        dist = inputPattern.sum() - overlapsWithProtos
      elif self.distanceMethod == "pctOverlapOfInput":
        dist = inputPatternSum - overlapsWithProtos
        if inputPatternSum > 0:
          dist /= inputPatternSum
      elif self.distanceMethod == "pctOverlapOfProto":
        overlapsWithProtos /= self._protoSizes
        dist = 1.0 - overlapsWithProtos
      elif self.distanceMethod == "pctOverlapOfLarger":
        maxVal = numpy.maximum(self._protoSizes, inputPatternSum)
        if maxVal.all() > 0:
          overlapsWithProtos /= maxVal
        dist = 1.0 - overlapsWithProtos
      elif self.distanceMethod == "norm":
        dist = self._Memory.vecLpDist(self.distanceNorm, inputPattern)
        distMax = dist.max()
        if distMax > 0:
          dist /= distMax
      else:
        raise RuntimeError("Unimplemented distance method %s" %
          self.distanceMethod)

    # Dense memory
    else:
      if self.distanceMethod == "norm":
        dist = numpy.power(numpy.abs(self._M - inputPattern), self.distanceNorm)
        dist = dist.sum(1)
        dist = numpy.power(dist, 1.0/self.distanceNorm)
        dist /= dist.max()
      else:
        raise RuntimeError ("Not implemented yet for dense storage....")

    return dist