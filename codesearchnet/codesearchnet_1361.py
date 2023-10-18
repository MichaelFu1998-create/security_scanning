def mostLikely(self, pred):
    """ Helper function to return a scalar value representing the most
        likely outcome given a probability distribution
    """
    if len(pred) == 1:
      return pred.keys()[0]

    mostLikelyOutcome = None
    maxProbability = 0

    for prediction, probability in pred.items():
      if probability > maxProbability:
        mostLikelyOutcome = prediction
        maxProbability = probability

    return mostLikelyOutcome