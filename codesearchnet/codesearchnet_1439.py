def isTemporal(inferenceType):
    """ Returns True if the inference type is 'temporal', i.e. requires a
    temporal memory in the network.
    """
    if InferenceType.__temporalInferenceTypes is None:
      InferenceType.__temporalInferenceTypes = \
                                set([InferenceType.TemporalNextStep,
                                     InferenceType.TemporalClassification,
                                     InferenceType.TemporalAnomaly,
                                     InferenceType.TemporalMultiStep,
                                     InferenceType.NontemporalMultiStep])

    return inferenceType in InferenceType.__temporalInferenceTypes