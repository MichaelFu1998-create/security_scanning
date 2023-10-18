def prettyPrintSequence(self, sequence, verbosity=1):
    """
    Pretty print a sequence.

    @param sequence  (list) Sequence
    @param verbosity (int)  Verbosity level

    @return (string) Pretty-printed text
    """
    text = ""

    for i in xrange(len(sequence)):
      pattern = sequence[i]

      if pattern == None:
        text += "<reset>"
        if i < len(sequence) - 1:
          text += "\n"
      else:
        text += self.patternMachine.prettyPrintPattern(pattern,
                                                       verbosity=verbosity)

    return text