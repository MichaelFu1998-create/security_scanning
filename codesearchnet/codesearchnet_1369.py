def getEncodedValues(self, inputData):
    """
    Returns the input in the same format as is returned by
    :meth:`.topDownCompute`. For most encoder types, this is the same as the
    input data. For instance, for scalar and category types, this corresponds to
    the numeric and string values, respectively, from the inputs. For datetime
    encoders, this returns the list of scalars for each of the sub-fields
    (timeOfDay, dayOfWeek, etc.)

    This method is essentially the same as :meth:`.getScalars` except that it
    returns strings.

    :param inputData: The input data in the format it is received from the data
                      source

    :return: A list of values, in the same format and in the same order as they
             are returned by :meth:`.topDownCompute`.
    """

    retVals = []

    if self.encoders is not None:
      for name, encoders, offset in self.encoders:
        values = encoders.getEncodedValues(self._getInputValue(inputData, name))

        if _isSequence(values):
          retVals.extend(values)
        else:
          retVals.append(values)
    else:
      if _isSequence(inputData):
        retVals.extend(inputData)
      else:
        retVals.append(inputData)

    return tuple(retVals)