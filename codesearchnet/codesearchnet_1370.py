def getBucketIndices(self, inputData):
    """
    Returns an array containing the sub-field bucket indices for each sub-field
    of the inputData. To get the associated field names for each of the buckets,
    call :meth:`.getScalarNames`.

    :param inputData: The data from the source. This is typically an object with
                 members.
    :return: array of bucket indices
    """

    retVals = []

    if self.encoders is not None:
      for (name, encoder, offset) in self.encoders:
        values = encoder.getBucketIndices(self._getInputValue(inputData, name))
        retVals.extend(values)
    else:
      assert False, "Should be implemented in base classes that are not " \
        "containers for other encoders"

    return retVals