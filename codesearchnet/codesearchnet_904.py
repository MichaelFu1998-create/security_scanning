def decode(self, encoded, parentFieldName=''):
    """ See the function description in base.py
    """

    assert (encoded[0:self.n] <= 1.0).all()

    resultString =  ""
    resultRanges = []

    overlaps =  (self.sdrs * encoded[0:self.n]).sum(axis=1)

    if self.verbosity >= 2:
      print "Overlaps for decoding:"
      for i in xrange(0, self.ncategories):
        print "%d %s" % (overlaps[i], self.categories[i])

    matchingCategories =  (overlaps > self.thresholdOverlap).nonzero()[0]

    for index in matchingCategories:
      if resultString != "":
        resultString += " "
      resultString +=  str(self.categories[index])
      resultRanges.append([int(index),int(index)])

    if parentFieldName != '':
      fieldName = "%s.%s" % (parentFieldName, self.name)
    else:
      fieldName = self.name
    return ({fieldName: (resultRanges, resultString)}, [fieldName])