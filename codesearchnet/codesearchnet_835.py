def setParameter(self, name, index, value):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.setParameter`.
    """
    if name == "learningMode":
      self.learningMode = bool(int(value))
    elif name == "inferenceMode":
      self.inferenceMode = bool(int(value))
    else:
      return PyRegion.setParameter(self, name, index, value)