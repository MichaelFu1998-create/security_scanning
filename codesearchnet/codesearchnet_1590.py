def decode(self, encoded, parentFieldName=''):
    """
    See the function description in base.py
    """

    # Get the scalar values from the underlying scalar encoder
    (fieldsDict, fieldNames) = self.encoder.decode(encoded)
    if len(fieldsDict) == 0:
      return (fieldsDict, fieldNames)

    # Expect only 1 field
    assert(len(fieldsDict) == 1)

    # Convert each range into normal space
    (inRanges, inDesc) = fieldsDict.values()[0]
    outRanges = []
    for (minV, maxV) in inRanges:
      outRanges.append((math.pow(10, minV),
                        math.pow(10, maxV)))

    # Generate a text description of the ranges
    desc = ""
    numRanges = len(outRanges)
    for i in xrange(numRanges):
      if outRanges[i][0] != outRanges[i][1]:
        desc += "%.2f-%.2f" % (outRanges[i][0], outRanges[i][1])
      else:
        desc += "%.2f" % (outRanges[i][0])
      if i < numRanges-1:
        desc += ", "

    # Return result
    if parentFieldName != '':
      fieldName = "%s.%s" % (parentFieldName, self.name)
    else:
      fieldName = self.name
    return ({fieldName: (outRanges, desc)}, [fieldName])