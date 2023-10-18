def __getDictMetaInfo(self, inferenceElement, inferenceDict):
    """Get field metadate information for inferences that are of dict type"""
    fieldMetaInfo = []
    inferenceLabel = InferenceElement.getLabel(inferenceElement)

    if InferenceElement.getInputElement(inferenceElement):
      fieldMetaInfo.append(FieldMetaInfo(name=inferenceLabel+".actual",
                                         type=FieldMetaType.string,
                                         special = ''))

    keys = sorted(inferenceDict.keys())
    for key in keys:
      fieldMetaInfo.append(FieldMetaInfo(name=inferenceLabel+"."+str(key),
                                         type=FieldMetaType.string,
                                         special=''))


    return fieldMetaInfo