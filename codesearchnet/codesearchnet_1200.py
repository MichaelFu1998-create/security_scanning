def read(cls, proto):
    """
    :param proto: capnp HTMPredictionModelProto message reader
    """
    obj = object.__new__(cls)
    # model.capnp
    super(HTMPredictionModel, obj).__init__(proto=proto.modelBase)

    # HTMPredictionModelProto.capnp
    obj._minLikelihoodThreshold = round(proto.minLikelihoodThreshold,
                                        EPSILON_ROUND)
    obj._maxPredictionsPerStep = proto.maxPredictionsPerStep

    network = Network.read(proto.network)
    obj._hasSP = ("SP" in network.regions)
    obj._hasTP = ("TM" in network.regions)
    obj._hasCL = ("Classifier" in network.regions)
    obj._netInfo = NetworkInfo(net=network, statsCollectors=[])

    obj.__spLearningEnabled = bool(proto.spLearningEnabled)
    obj.__tpLearningEnabled = bool(proto.tpLearningEnabled)
    obj.__numRunCalls = proto.numRunCalls

    obj._classifierInputEncoder = None
    if proto.predictedFieldIdx.which() == "none":
      obj._predictedFieldIdx = None
    else:
      obj._predictedFieldIdx = proto.predictedFieldIdx.value
    if proto.predictedFieldName.which() == "none":
      obj._predictedFieldName = None
    else:
      obj._predictedFieldName = proto.predictedFieldName.value
    obj._numFields = proto.numFields
    if proto.numFields.which() == "none":
      obj._numFields = None
    else:
      obj._numFields = proto.numFields.value
    obj.__trainSPNetOnlyIfRequested = proto.trainSPNetOnlyIfRequested
    obj.__finishedLearning = proto.finishedLearning
    obj._input = None
    sensor = network.regions['sensor'].getSelf()
    sensor.dataSource = DataBuffer()
    network.initialize()


    obj.__logger = initLogger(obj)
    obj.__logger.debug("Instantiating %s." % obj.__myClassName)

    # Mark end of restoration from state
    obj.__restoringFromState = False
    obj.__restoringFromV1 = False

    return obj