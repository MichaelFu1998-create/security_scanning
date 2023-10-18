def getOutputElementCount(self, name):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.getOutputElementCount`.
    """
    if name == 'categoriesOut':
      return self.maxCategoryCount
    elif name == 'categoryProbabilitiesOut':
      return self.maxCategoryCount
    elif name == 'bestPrototypeIndices':
      return self._bestPrototypeIndexCount if self._bestPrototypeIndexCount else 0
    else:
      raise Exception('Unknown output: ' + name)