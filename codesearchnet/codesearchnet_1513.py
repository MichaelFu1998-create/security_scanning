def read(cls, proto):
    """Deserialize via capnp

    :param proto: capnp PreviousValueModelProto message reader

    :returns: new instance of PreviousValueModel deserialized from the given
              proto
    """
    instance = object.__new__(cls)
    super(PreviousValueModel, instance).__init__(proto=proto.modelBase)

    instance._logger = opf_utils.initLogger(instance)
    if len(proto.predictedField):
      instance._predictedField = proto.predictedField
    else:
      instance._predictedField = None
    instance._fieldNames = list(proto.fieldNames)
    instance._fieldTypes = list(proto.fieldTypes)
    instance._predictionSteps = list(proto.predictionSteps)

    return instance