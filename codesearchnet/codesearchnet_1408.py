def getAdaptiveSVDDims(self, singularValues, fractionOfMax=0.001):
    """
    Compute the number of eigenvectors (singularValues) to keep.

    :param singularValues:
    :param fractionOfMax:
    :return:
    """
    v = singularValues/singularValues[0]
    idx = numpy.where(v<fractionOfMax)[0]
    if len(idx):
      print "Number of PCA dimensions chosen: ", idx[0], "out of ", len(v)
      return idx[0]
    else:
      print "Number of PCA dimensions chosen: ", len(v)-1, "out of ", len(v)
      return len(v)-1