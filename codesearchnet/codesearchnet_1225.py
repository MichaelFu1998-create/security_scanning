def newPosition(self, globalBestPosition, rng):
    """See comments in base class."""
    # Compute the mean score per choice.
    numChoices = len(self.choices)
    meanScorePerChoice = []
    overallSum = 0
    numResults = 0

    for i in range(numChoices):
      if len(self._resultsPerChoice[i]) > 0:
        data = numpy.array(self._resultsPerChoice[i])
        meanScorePerChoice.append(data.mean())
        overallSum += data.sum()
        numResults += data.size
      else:
        meanScorePerChoice.append(None)

    if numResults == 0:
      overallSum = 1.0
      numResults = 1

    # For any choices we don't have a result for yet, set to the overall mean.
    for i in range(numChoices):
      if meanScorePerChoice[i] is None:
        meanScorePerChoice[i] = overallSum / numResults

    # Now, pick a new choice based on the above probabilities. Note that the
    #  best result is the lowest result. We want to make it more likely to
    #  pick the choice that produced the lowest results. So, we need to invert
    #  the scores (someLargeNumber - score).
    meanScorePerChoice = numpy.array(meanScorePerChoice)

    # Invert meaning.
    meanScorePerChoice = (1.1 * meanScorePerChoice.max()) - meanScorePerChoice

    # If you want the scores to quickly converge to the best choice, raise the
    # results to a power. This will cause lower scores to become lower
    # probability as you see more results, until it eventually should
    # assymptote to only choosing the best choice.
    if self._fixEarly:
      meanScorePerChoice **= (numResults * self._fixEarlyFactor / numChoices)
    # Normalize.
    total = meanScorePerChoice.sum()
    if total == 0:
      total = 1.0
    meanScorePerChoice /= total

    # Get distribution and choose one based on those probabilities.
    distribution = meanScorePerChoice.cumsum()
    r = rng.random() * distribution[-1]
    choiceIdx = numpy.where(r <= distribution)[0][0]

    self._positionIdx = choiceIdx
    return self.getPosition()