def isTemporal(inferenceElement):
    """ Returns True if the inference from this timestep is predicted the input
    for the NEXT timestep.

    NOTE: This should only be checked IF THE MODEL'S INFERENCE TYPE IS ALSO
    TEMPORAL. That is, a temporal model CAN have non-temporal inference elements,
    but a non-temporal model CANNOT have temporal inference elements
    """
    if InferenceElement.__temporalInferenceElements is None:
      InferenceElement.__temporalInferenceElements = \
                                set([InferenceElement.prediction])

    return inferenceElement in InferenceElement.__temporalInferenceElements