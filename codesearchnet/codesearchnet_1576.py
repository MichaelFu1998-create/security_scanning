def closenessScores(self, expValues, actValues, **kwargs):
    """
    Does a bitwise compare of the two bitmaps and returns a fractonal
    value between 0 and 1 of how similar they are.

    - ``1`` => identical
    - ``0`` => no overlaping bits

    ``kwargs`` will have the keyword "fractional", which is assumed by this
    encoder.
    """
    ratio = 1.0
    esum = int(expValues.sum())
    asum = int(actValues.sum())
    if asum > esum:
      diff = asum - esum
      if diff < esum:
        ratio = 1 - diff/float(esum)
      else:
        ratio = 1/float(diff)

    olap = expValues & actValues
    osum = int(olap.sum())
    if esum == 0:
      r = 0.0
    else:
      r = osum/float(esum)
    r = r * ratio

    return numpy.array([r])