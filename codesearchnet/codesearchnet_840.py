def getOutputElementCount(self, outputName):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.getOutputElementCount`.
    """
    if outputName == "categoriesOut":
      return len(self.stepsList)
    elif outputName == "probabilities":
      return len(self.stepsList) * self.maxCategoryCount
    elif outputName == "actualValues":
      return self.maxCategoryCount
    else:
      raise ValueError("Unknown output {}.".format(outputName))