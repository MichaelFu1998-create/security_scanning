def getParameter(self, name, index=-1):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.getParameter`.
    """
    if name == "patternCount":
      return self._knn._numPatterns
    elif name == "patternMatrix":
      return self._getPatternMatrix()
    elif name == "k":
      return self._knn.k
    elif name == "distanceNorm":
      return self._knn.distanceNorm
    elif name == "distanceMethod":
      return self._knn.distanceMethod
    elif name == "distThreshold":
      return self._knn.distThreshold
    elif name == "inputThresh":
      return self._knn.binarizationThreshold
    elif name == "doBinarization":
      return self._knn.doBinarization
    elif name == "useSparseMemory":
      return self._knn.useSparseMemory
    elif name == "sparseThreshold":
      return self._knn.sparseThreshold
    elif name == "winnerCount":
      return self._knn.numWinners
    elif name == "relativeThreshold":
      return self._knn.relativeThreshold
    elif name == "SVDSampleCount":
      v = self._knn.numSVDSamples
      return v if v is not None else 0
    elif name == "SVDDimCount":
      v = self._knn.numSVDDims
      return v if v is not None else 0
    elif name == "fractionOfMax":
      v = self._knn.fractionOfMax
      return v if v is not None else 0
    elif name == "useAuxiliary":
      return self._useAuxiliary
    elif name == "justUseAuxiliary":
      return self._justUseAuxiliary
    elif name == "doSphering":
      return self._doSphering
    elif name == "cellsPerCol":
      return self._knn.cellsPerCol
    elif name == "maxStoredPatterns":
      return self.maxStoredPatterns
    elif name == 'categoryRecencyList':
      return self._knn._categoryRecencyList
    else:
      # If any spec parameter name is the same as an attribute, this call
      # will get it automatically, e.g. self.learningMode
      return PyRegion.getParameter(self, name, index)