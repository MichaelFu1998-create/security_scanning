def prettyPrintPattern(self, bits, verbosity=1):
    """
    Pretty print a pattern.

    @param bits      (set) Indices of on bits
    @param verbosity (int) Verbosity level

    @return (string) Pretty-printed text
    """
    numberMap = self.numberMapForBits(bits)
    text = ""

    numberList = []
    numberItems = sorted(numberMap.iteritems(),
                         key=lambda (number, bits): len(bits),
                         reverse=True)

    for number, bits in numberItems:

      if verbosity > 2:
        strBits = [str(n) for n in bits]
        numberText = "{0} (bits: {1})".format(number, ",".join(strBits))
      elif verbosity > 1:
        numberText = "{0} ({1} bits)".format(number, len(bits))
      else:
        numberText = str(number)

      numberList.append(numberText)

    text += "[{0}]".format(", ".join(numberList))

    return text