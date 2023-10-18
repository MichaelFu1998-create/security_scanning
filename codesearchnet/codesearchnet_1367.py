def getEncoderList(self):
    """
    :return: a reference to each sub-encoder in this encoder. They are
             returned in the same order as they are for :meth:`.getScalarNames`
             and :meth:`.getScalars`.

    """
    if hasattr(self, '_flattenedEncoderList') and \
        self._flattenedEncoderList is not None:

      return self._flattenedEncoderList

    encoders = []

    if self.encoders is not None:
      for (name, encoder, offset) in self.encoders:
        subEncoders = encoder.getEncoderList()
        encoders.extend(subEncoders)
    else:
      encoders.append(self)

    self._flattenedEncoderList = encoders
    return encoders