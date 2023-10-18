def write(self, proto):
    """ Serialize via capnp

    :param proto: capnp PreviousValueModelProto message builder
    """
    super(PreviousValueModel, self).writeBaseToProto(proto.modelBase)

    proto.fieldNames = self._fieldNames
    proto.fieldTypes = self._fieldTypes
    if self._predictedField:
      proto.predictedField = self._predictedField
    proto.predictionSteps = self._predictionSteps