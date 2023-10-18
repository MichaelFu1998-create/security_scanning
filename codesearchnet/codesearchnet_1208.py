def _setMinAndMax(self, input, learn):
    """
    Potentially change the minval and maxval using input.
    **The learn flag is currently not supported by cla regions.**
    """

    self.slidingWindow.next(input)

    if self.minval is None and self.maxval is None:
      self.minval = input
      self.maxval = input+1   #When the min and max and unspecified and only one record has been encoded
      self._setEncoderParams()

    elif learn:
      sorted = self.slidingWindow.getSlidingWindow()
      sorted.sort()

      minOverWindow = sorted[0]
      maxOverWindow = sorted[len(sorted)-1]

      if minOverWindow < self.minval:
        #initialBump = abs(self.minval-minOverWindow)*(1-(min(self.recordNum, 200.0)/200.0))*2      #decrement minval more aggressively in the beginning
        if self.verbosity >= 2:
          print "Input %s=%.2f smaller than minval %.2f. Adjusting minval to %.2f"\
                          % (self.name, input, self.minval, minOverWindow)
        self.minval = minOverWindow       #-initialBump
        self._setEncoderParams()

      if maxOverWindow > self.maxval:
        #initialBump = abs(self.maxval-maxOverWindow)*(1-(min(self.recordNum, 200.0)/200.0))*2     #decrement maxval more aggressively in the beginning
        if self.verbosity >= 2:
          print "Input %s=%.2f greater than maxval %.2f. Adjusting maxval to %.2f" \
                          % (self.name, input, self.maxval, maxOverWindow)
        self.maxval = maxOverWindow       #+initialBump
        self._setEncoderParams()