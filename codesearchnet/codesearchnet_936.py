def readFromProto(cls, proto):
    """
    Overrides :meth:`~nupic.bindings.regions.PyRegion.PyRegion.readFromProto`.

    Read state from proto object.
    
    :param proto: SPRegionProto capnproto object
    """
    instance = cls(proto.columnCount, proto.inputWidth)

    instance.spatialImp = proto.spatialImp
    instance.learningMode = proto.learningMode
    instance.inferenceMode = proto.inferenceMode
    instance.anomalyMode = proto.anomalyMode
    instance.topDownMode = proto.topDownMode

    spatialImp = proto.spatialImp
    instance._sfdr = getSPClass(spatialImp).read(proto.spatialPooler)

    return instance