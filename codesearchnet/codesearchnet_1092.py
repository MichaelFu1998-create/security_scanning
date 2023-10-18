def decode(self, encoded, parentFieldName=''):
    """ See the function description in base.py
    """

    # Get the scalar values from the underlying scalar encoder
    (fieldsDict, fieldNames) = self.encoder.decode(encoded)
    if len(fieldsDict) == 0:
      return (fieldsDict, fieldNames)

    # Expect only 1 field
    assert(len(fieldsDict) == 1)

    # Get the list of categories the scalar values correspond to and
    #  generate the description from the category name(s).
    (inRanges, inDesc) = fieldsDict.values()[0]
    outRanges = []
    desc = ""
    for (minV, maxV) in inRanges:
      minV = int(round(minV))
      maxV = int(round(maxV))
      outRanges.append((minV, maxV))
      while minV <= maxV:
        if len(desc) > 0:
          desc += ", "
        desc += self.indexToCategory[minV]
        minV += 1

    # Return result
    if parentFieldName != '':
      fieldName = "%s.%s" % (parentFieldName, self.name)
    else:
      fieldName = self.name
    return ({fieldName: (outRanges, desc)}, [fieldName])