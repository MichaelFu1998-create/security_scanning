def getBucketIndices(self, inpt):
    """
    See the function description in base.py
    """

    # Get the scaled value
    scaledVal = self._getScaledValue(inpt)

    if scaledVal is None:
      return [None]
    else:
      return self.encoder.getBucketIndices(scaledVal)