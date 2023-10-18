def encodeIntoArray(self, inputVal, outputVal):
    """See method description in base.py"""
    if len(inputVal) != len(outputVal):
      raise ValueError("Different input (%i) and output (%i) sizes." % (
          len(inputVal), len(outputVal)))

    if self.w is not None and sum(inputVal) != self.w:
      raise ValueError("Input has %i bits but w was set to %i." % (
          sum(inputVal), self.w))

    outputVal[:] = inputVal[:]

    if self.verbosity >= 2:
      print "input:", inputVal, "output:", outputVal
      print "decoded:", self.decodedToStr(self.decode(outputVal))