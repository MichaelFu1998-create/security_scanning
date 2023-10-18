def _getScaledValue(self, inpt):
    """
    Convert the input, which is in normal space, into log space
    """
    if inpt == SENTINEL_VALUE_FOR_MISSING_DATA:
      return None
    else:
      val = inpt
      if val < self.minval:
        val = self.minval
      elif val > self.maxval:
        val = self.maxval

      scaledVal = math.log10(val)
      return scaledVal