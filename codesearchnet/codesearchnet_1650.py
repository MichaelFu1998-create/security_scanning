def encodeIntoArray(self, input, output, learn=True):
    """ See method description in base.py """

    if input is not None and not isinstance(input, numbers.Number):
      raise TypeError(
          "Expected a scalar input but got input of type %s" % type(input))

    if type(input) is float and math.isnan(input):
      input = SENTINEL_VALUE_FOR_MISSING_DATA

    # Get the bucket index to use
    bucketIdx = self._getFirstOnBit(input)[0]

    if bucketIdx is None:
      # None is returned for missing value
      output[0:self.n] = 0  #TODO: should all 1s, or random SDR be returned instead?

    else:
      # The bucket index is the index of the first bit to set in the output
      output[:self.n] = 0
      minbin = bucketIdx
      maxbin = minbin + 2*self.halfwidth
      if self.periodic:
        # Handle the edges by computing wrap-around
        if maxbin >= self.n:
          bottombins = maxbin - self.n + 1
          output[:bottombins] = 1
          maxbin = self.n - 1
        if minbin < 0:
          topbins = -minbin
          output[self.n - topbins:self.n] = 1
          minbin = 0

      assert minbin >= 0
      assert maxbin < self.n
      # set the output (except for periodic wraparound)
      output[minbin:maxbin + 1] = 1

    # Debug the decode() method
    if self.verbosity >= 2:
      print
      print "input:", input
      print "range:", self.minval, "-", self.maxval
      print "n:", self.n, "w:", self.w, "resolution:", self.resolution, \
            "radius", self.radius, "periodic:", self.periodic
      print "output:",
      self.pprint(output)
      print "input desc:", self.decodedToStr(self.decode(output))