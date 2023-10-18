def _getClassifierInputRecord(self, inputRecord):
    """
    inputRecord - dict containing the input to the sensor

    Return a 'ClassifierInput' object, which contains the mapped
    bucket index for input Record
    """
    absoluteValue = None
    bucketIdx = None

    if self._predictedFieldName is not None and self._classifierInputEncoder is not None:
      absoluteValue = inputRecord[self._predictedFieldName]
      bucketIdx = self._classifierInputEncoder.getBucketIndices(absoluteValue)[0]

    return ClassifierInput(dataRow=absoluteValue,
                           bucketIndex=bucketIdx)