def _getGroundTruth(self, inferenceElement):
    """
    Get the actual value for this field

    Parameters:
    -----------------------------------------------------------------------
    sensorInputElement:       The inference element (part of the inference) that
                            is being used for this metric
    """
    sensorInputElement = InferenceElement.getInputElement(inferenceElement)
    if sensorInputElement is None:
      return None
    return getattr(self.__currentGroundTruth.sensorInput, sensorInputElement)