def getOutputElementCount(self, name):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.getOutputElementCount`.
    """
    if name == 'bottomUpOut':
      return self.outputWidth
    elif name == 'topDownOut':
      return self.columnCount
    elif name == 'lrnActiveStateT':
      return self.outputWidth
    elif name == "activeCells":
      return self.outputWidth
    elif name == "predictedActiveCells":
      return self.outputWidth
    else:
      raise Exception("Invalid output name specified")