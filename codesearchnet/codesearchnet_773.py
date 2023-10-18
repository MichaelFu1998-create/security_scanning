def getParameter(self, name, index=-1):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.getParameter`.
    """
    if name == "trainRecords":
      return self.trainRecords
    elif name == "anomalyThreshold":
      return self.anomalyThreshold
    elif name == "activeColumnCount":
      return self._activeColumnCount
    elif name == "classificationMaxDist":
      return self._classificationMaxDist
    else:
      # If any spec parameter name is the same as an attribute, this call
      # will get it automatically, e.g. self.learningMode
      return PyRegion.getParameter(self, name, index)