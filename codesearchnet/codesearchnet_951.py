def writeToProto(self, proto):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.writeToProto`.

    Write state to proto object.

    :param proto: TMRegionProto capnproto object
    """
    proto.temporalImp = self.temporalImp
    proto.columnCount = self.columnCount
    proto.inputWidth = self.inputWidth
    proto.cellsPerColumn = self.cellsPerColumn
    proto.learningMode = self.learningMode
    proto.inferenceMode = self.inferenceMode
    proto.anomalyMode = self.anomalyMode
    proto.topDownMode = self.topDownMode
    proto.computePredictedActiveCellIndices = (
      self.computePredictedActiveCellIndices)
    proto.orColumnOutputs = self.orColumnOutputs

    if self.temporalImp == "py":
      tmProto = proto.init("backtrackingTM")
    elif self.temporalImp == "cpp":
      tmProto = proto.init("backtrackingTMCpp")
    elif self.temporalImp == "tm_py":
      tmProto = proto.init("temporalMemory")
    elif self.temporalImp == "tm_cpp":
      tmProto = proto.init("temporalMemory")
    else:
      raise TypeError(
          "Unsupported temporalImp for capnp serialization: {}".format(
              self.temporalImp))

    self._tfdr.write(tmProto)