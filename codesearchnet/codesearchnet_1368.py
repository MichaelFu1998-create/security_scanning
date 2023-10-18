def getScalars(self, inputData):
    """
    Returns a numpy array containing the sub-field scalar value(s) for
    each sub-field of the ``inputData``. To get the associated field names for
    each of the scalar values, call :meth:`.getScalarNames()`.

    For a simple scalar encoder, the scalar value is simply the input unmodified.
    For category encoders, it is the scalar representing the category string
    that is passed in. For the datetime encoder, the scalar value is the
    the number of seconds since epoch.

    The intent of the scalar representation of a sub-field is to provide a
    baseline for measuring error differences. You can compare the scalar value
    of the inputData with the scalar value returned from :meth:`.topDownCompute`
    on a top-down representation to evaluate prediction accuracy, for example.

    :param inputData: The data from the source. This is typically an object with
                 members
    :return: array of scalar values
    """

    retVals = numpy.array([])

    if self.encoders is not None:
      for (name, encoder, offset) in self.encoders:
        values = encoder.getScalars(self._getInputValue(inputData, name))
        retVals = numpy.hstack((retVals, values))
    else:
      retVals = numpy.hstack((retVals, inputData))

    return retVals