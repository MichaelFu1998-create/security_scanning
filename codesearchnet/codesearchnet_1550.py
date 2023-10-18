def writeBaseToProto(self, proto):
    """Save the state maintained by the Model base class

    :param proto: capnp ModelProto message builder
    """
    inferenceType = self.getInferenceType()
    # lower-case first letter to be compatible with capnproto enum naming
    inferenceType = inferenceType[:1].lower() + inferenceType[1:]
    proto.inferenceType = inferenceType

    proto.numPredictions = self._numPredictions

    proto.learningEnabled = self.__learningEnabled
    proto.inferenceEnabled = self.__inferenceEnabled
    proto.inferenceArgs = json.dumps(self.__inferenceArgs)