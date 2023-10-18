def encodeIntoArray(self, value, output):
    """ See method description in base.py """
    denseInput = numpy.zeros(output.shape)
    try:
      denseInput[value] = 1
    except IndexError:
      if isinstance(value, numpy.ndarray):
        raise ValueError(
            "Numpy array must have integer dtype but got {}".format(
                value.dtype))
      raise
    super(SparsePassThroughEncoder, self).encodeIntoArray(denseInput, output)