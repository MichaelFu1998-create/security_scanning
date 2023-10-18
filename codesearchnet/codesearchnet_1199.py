def write(self, proto):
    """
    :param proto: capnp HTMPredictionModelProto message builder
    """
    super(HTMPredictionModel, self).writeBaseToProto(proto.modelBase)

    proto.numRunCalls = self.__numRunCalls
    proto.minLikelihoodThreshold = self._minLikelihoodThreshold
    proto.maxPredictionsPerStep = self._maxPredictionsPerStep

    self._netInfo.net.write(proto.network)
    proto.spLearningEnabled = self.__spLearningEnabled
    proto.tpLearningEnabled = self.__tpLearningEnabled
    if self._predictedFieldIdx is None:
      proto.predictedFieldIdx.none = None
    else:
      proto.predictedFieldIdx.value = self._predictedFieldIdx
    if self._predictedFieldName is None:
      proto.predictedFieldName.none = None
    else:
      proto.predictedFieldName.value = self._predictedFieldName
    if self._numFields is None:
      proto.numFields.none = None
    else:
      proto.numFields.value = self._numFields
    proto.trainSPNetOnlyIfRequested = self.__trainSPNetOnlyIfRequested
    proto.finishedLearning = self.__finishedLearning