def copy(self):
    """Return a clone object.

    Return a copy ('clone') of the md5 object. This can be used
    to efficiently compute the digests of strings that share
    a common initial substring.
    """
    if 0:  # set this to 1 to make the flow space crash
      return copy.deepcopy(self)
    clone = self.__class__()
    clone.length = self.length
    clone.count = [] + self.count[:]
    clone.input = [] + self.input
    clone.A = self.A
    clone.B = self.B
    clone.C = self.C
    clone.D = self.D
    return clone