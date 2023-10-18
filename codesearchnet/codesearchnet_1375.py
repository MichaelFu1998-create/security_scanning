def pprint(self, output, prefix=""):
    """
    Pretty-print the encoded output using ascii art.

    :param output: to print
    :param prefix: printed before the header if specified
    """
    print prefix,
    description = self.getDescription() + [("end", self.getWidth())]
    for i in xrange(len(description) - 1):
      offset = description[i][1]
      nextoffset = description[i+1][1]
      print "%s |" % bitsToString(output[offset:nextoffset]),
    print