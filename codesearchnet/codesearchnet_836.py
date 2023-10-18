def writeToProto(self, proto):
    """
    Write state to proto object.

    :param proto: SDRClassifierRegionProto capnproto object
    """
    proto.implementation = self.implementation
    proto.steps = self.steps
    proto.alpha = self.alpha
    proto.verbosity = self.verbosity
    proto.maxCategoryCount = self.maxCategoryCount
    proto.learningMode = self.learningMode
    proto.inferenceMode = self.inferenceMode
    proto.recordNum = self.recordNum

    self._sdrClassifier.write(proto.sdrClassifier)