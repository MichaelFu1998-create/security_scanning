def readFromProto(cls, proto):
    """    
    Overrides :meth:`nupic.bindings.regions.PyRegion.PyRegion.readFromProto`.
    """
    instance = cls()

    instance.encoder = MultiEncoder.read(proto.encoder)
    if proto.disabledEncoder is not None:
      instance.disabledEncoder = MultiEncoder.read(proto.disabledEncoder)
    instance.topDownMode = bool(proto.topDownMode)
    instance.verbosity = proto.verbosity
    instance.numCategories = proto.numCategories

    return instance