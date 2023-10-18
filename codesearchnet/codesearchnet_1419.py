def writeToProto(self, proto):
    """
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.writeToProto`.
    """
    self.encoder.write(proto.encoder)
    if self.disabledEncoder is not None:
      self.disabledEncoder.write(proto.disabledEncoder)
    proto.topDownMode = int(self.topDownMode)
    proto.verbosity = self.verbosity
    proto.numCategories = self.numCategories