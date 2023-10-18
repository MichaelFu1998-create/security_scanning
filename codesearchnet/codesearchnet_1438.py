def getMaxDelay(inferences):
    """
    Returns the maximum delay for the InferenceElements in the inference
    dictionary

    Parameters:
    -----------------------------------------------------------------------
    inferences:   A dictionary where the keys are InferenceElements
    """
    maxDelay = 0
    for inferenceElement, inference in inferences.iteritems():
      if isinstance(inference, dict):
        for key in inference.iterkeys():
          maxDelay = max(InferenceElement.getTemporalDelay(inferenceElement,
                                                            key),
                         maxDelay)
      else:
        maxDelay = max(InferenceElement.getTemporalDelay(inferenceElement),
                       maxDelay)


    return maxDelay