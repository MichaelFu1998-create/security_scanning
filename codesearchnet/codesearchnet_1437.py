def getTemporalDelay(inferenceElement, key=None):
    """ Returns the number of records that elapse between when an inference is
    made and when the corresponding input record will appear. For example, a
    multistep prediction for 3 timesteps out will have a delay of 3


    Parameters:
    -----------------------------------------------------------------------

    inferenceElement:   The InferenceElement value being delayed
    key:                If the inference is a dictionary type, this specifies
                        key for the sub-inference that is being delayed
    """
    # -----------------------------------------------------------------------
    # For next step prediction, we shift by 1
    if inferenceElement in (InferenceElement.prediction,
                            InferenceElement.encodings):
      return 1
    # -----------------------------------------------------------------------
    # For classification, anomaly scores, the inferences immediately succeed the
    # inputs
    if inferenceElement in (InferenceElement.anomalyScore,
                            InferenceElement.anomalyLabel,
                            InferenceElement.classification,
                            InferenceElement.classConfidences):
      return 0
    # -----------------------------------------------------------------------
    # For multistep prediction, the delay is based on the key in the inference
    # dictionary
    if inferenceElement in (InferenceElement.multiStepPredictions,
                            InferenceElement.multiStepBestPredictions):
      return int(key)

    # -----------------------------------------------------------------------
    # default: return 0
    return 0