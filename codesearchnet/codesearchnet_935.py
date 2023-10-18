def writeToProto(self, proto):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.writeToProto`.

    Write state to proto object.

    :param proto: SPRegionProto capnproto object
    """
    proto.spatialImp = self.spatialImp
    proto.columnCount = self.columnCount
    proto.inputWidth = self.inputWidth
    proto.learningMode = 1 if self.learningMode else 0
    proto.inferenceMode = 1 if self.inferenceMode else 0
    proto.anomalyMode = 1 if self.anomalyMode else 0
    proto.topDownMode = 1 if self.topDownMode else 0

    self._sfdr.write(proto.spatialPooler)