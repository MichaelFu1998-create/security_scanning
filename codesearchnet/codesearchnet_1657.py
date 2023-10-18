def closenessScores(self, expValues, actValues, fractional=True):
    """ See the function description in base.py
    """

    expValue = expValues[0]
    actValue = actValues[0]
    if self.periodic:
      expValue = expValue % self.maxval
      actValue = actValue % self.maxval

    err = abs(expValue - actValue)
    if self.periodic:
      err = min(err, self.maxval - err)
    if fractional:
      pctErr = float(err) / (self.maxval - self.minval)
      pctErr = min(1.0, pctErr)
      closeness = 1.0 - pctErr
    else:
      closeness = err

    return numpy.array([closeness])