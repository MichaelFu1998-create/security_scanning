def encodedBitDescription(self, bitOffset, formatted=False):
    """
    Return a description of the given bit in the encoded output.
    This will include the field name and the offset within the field.

    :param bitOffset:      Offset of the bit to get the description of
    :param formatted:      If True, the bitOffset is w.r.t. formatted output,
                          which includes separators
    :return:             tuple(``fieldName``, ``offsetWithinField``)
    """

    # Find which field it's in
    (prevFieldName, prevFieldOffset) = (None, None)
    description = self.getDescription()
    for i in xrange(len(description)):
      (name, offset) = description[i]
      if formatted:
        offset = offset + i
        if bitOffset == offset-1:
          prevFieldName = "separator"
          prevFieldOffset = bitOffset
          break

      if bitOffset < offset:
        break
      (prevFieldName, prevFieldOffset) = (name, offset)

    # Return the field name and offset within the field
    # return (fieldName, bitOffset - fieldOffset)
    width = self.getDisplayWidth() if formatted else self.getWidth()

    if prevFieldOffset is None or bitOffset > self.getWidth():
      raise IndexError("Bit is outside of allowable range: [0 - %d]" % width)

    return (prevFieldName, bitOffset - prevFieldOffset)