def encode(self, inputData):
    """Convenience wrapper for :meth:`.encodeIntoArray`.

    This may be less efficient because it allocates a new numpy array every
    call.

    :param inputData: input data to be encoded
    :return: a numpy array with the encoded representation of inputData
    """
    output = numpy.zeros((self.getWidth(),), dtype=defaultDtype)
    self.encodeIntoArray(inputData, output)
    return output