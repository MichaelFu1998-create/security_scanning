def __getListMetaInfo(self, inferenceElement):
    """ Get field metadata information for inferences that are of list type
    TODO: Right now we assume list inferences are associated with the input field
    metadata
    """
    fieldMetaInfo = []
    inferenceLabel = InferenceElement.getLabel(inferenceElement)

    for inputFieldMeta in self.__inputFieldsMeta:
      if InferenceElement.getInputElement(inferenceElement):
        outputFieldMeta = FieldMetaInfo(
          name=inputFieldMeta.name + ".actual",
          type=inputFieldMeta.type,
          special=inputFieldMeta.special
        )

      predictionField = FieldMetaInfo(
        name=inputFieldMeta.name + "." + inferenceLabel,
        type=inputFieldMeta.type,
        special=inputFieldMeta.special
      )

      fieldMetaInfo.append(outputFieldMeta)
      fieldMetaInfo.append(predictionField)

    return fieldMetaInfo