def readFromProto(cls, proto):
    """
    Read state from proto object.

    :param proto: SDRClassifierRegionProto capnproto object
    """
    instance = cls()

    instance.implementation = proto.implementation
    instance.steps = proto.steps
    instance.stepsList = [int(i) for i in proto.steps.split(",")]
    instance.alpha = proto.alpha
    instance.verbosity = proto.verbosity
    instance.maxCategoryCount = proto.maxCategoryCount

    instance._sdrClassifier = SDRClassifierFactory.read(proto)

    instance.learningMode = proto.learningMode
    instance.inferenceMode = proto.inferenceMode
    instance.recordNum = proto.recordNum

    return instance