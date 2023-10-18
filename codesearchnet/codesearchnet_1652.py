def _generateRangeDescription(self, ranges):
    """generate description from a text description of the ranges"""
    desc = ""
    numRanges = len(ranges)
    for i in xrange(numRanges):
      if ranges[i][0] != ranges[i][1]:
        desc += "%.2f-%.2f" % (ranges[i][0], ranges[i][1])
      else:
        desc += "%.2f" % (ranges[i][0])
      if i < numRanges - 1:
        desc += ", "
    return desc