def closenessScores(self, expValues, actValues, fractional=True):
    """
    See the function description in base.py
    """

    # Compute the percent error in log space
    if expValues[0] > 0:
      expValue = math.log10(expValues[0])
    else:
      expValue = self.minScaledValue

    if actValues  [0] > 0:
      actValue = math.log10(actValues[0])
    else:
      actValue = self.minScaledValue

    if fractional:
      err = abs(expValue - actValue)
      pctErr = err / (self.maxScaledValue - self.minScaledValue)
      pctErr = min(1.0, pctErr)
      closeness = 1.0 - pctErr
    else:
      err = abs(expValue - actValue)
      closeness = err

    #print "log::", "expValue:", expValues[0], "actValue:", actValues[0], \
    #      "closeness", closeness
    #import pdb; pdb.set_trace()
    return numpy.array([closeness])