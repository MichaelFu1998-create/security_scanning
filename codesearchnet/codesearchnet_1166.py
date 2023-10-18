def inferSingleStep(self, patternNZ, weightMatrix):
    """
    Perform inference for a single step. Given an SDR input and a weight
    matrix, return a predicted distribution.

    :param patternNZ: list of the active indices from the output below
    :param weightMatrix: numpy array of the weight matrix
    :return: numpy array of the predicted class label distribution
    """
    outputActivation = weightMatrix[patternNZ].sum(axis=0)

    # softmax normalization
    outputActivation = outputActivation - numpy.max(outputActivation)
    expOutputActivation = numpy.exp(outputActivation)
    predictDist = expOutputActivation / numpy.sum(expOutputActivation)
    return predictDist