def encodeIntoArray(self, inpt, output):
    """
    See the function description in base.py
    """

    # Get the scaled value
    scaledVal = self._getScaledValue(inpt)

    if scaledVal is None:
      output[0:] = 0
    else:
      self.encoder.encodeIntoArray(scaledVal, output)

      if self.verbosity >= 2:
        print "input:", inpt, "scaledVal:", scaledVal, "output:", output
        print "decoded:", self.decodedToStr(self.decode(output))