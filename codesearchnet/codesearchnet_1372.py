def getFieldDescription(self, fieldName):
    """
    Return the offset and length of a given field within the encoded output.

    :param fieldName: Name of the field
    :return: tuple(``offset``, ``width``) of the field within the encoded output
    """

    # Find which field it's in
    description = self.getDescription() + [("end", self.getWidth())]
    for i in xrange(len(description)):
      (name, offset) = description[i]
      if (name == fieldName):
        break

    if i >= len(description)-1:
      raise RuntimeError("Field name %s not found in this encoder" % fieldName)

    # Return the offset and width
    return (offset, description[i+1][1] - offset)