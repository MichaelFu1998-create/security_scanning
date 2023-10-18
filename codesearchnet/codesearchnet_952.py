def readFromProto(cls, proto):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.readFromProto`.

    Read state from proto object.

    :param proto: TMRegionProto capnproto object
    """
    instance = cls(proto.columnCount, proto.inputWidth, proto.cellsPerColumn)

    instance.temporalImp = proto.temporalImp
    instance.learningMode = proto.learningMode
    instance.inferenceMode = proto.inferenceMode
    instance.anomalyMode = proto.anomalyMode
    instance.topDownMode = proto.topDownMode
    instance.computePredictedActiveCellIndices = (
      proto.computePredictedActiveCellIndices)
    instance.orColumnOutputs = proto.orColumnOutputs

    if instance.temporalImp == "py":
      tmProto = proto.backtrackingTM
    elif instance.temporalImp == "cpp":
      tmProto = proto.backtrackingTMCpp
    elif instance.temporalImp == "tm_py":
      tmProto = proto.temporalMemory
    elif instance.temporalImp == "tm_cpp":
      tmProto = proto.temporalMemory
    else:
      raise TypeError(
          "Unsupported temporalImp for capnp serialization: {}".format(
              instance.temporalImp))

    instance._tfdr = _getTPClass(proto.temporalImp).read(tmProto)

    return instance