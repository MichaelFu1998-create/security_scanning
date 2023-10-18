def decodedToStr(self, decodeResults):
    """
    Return a pretty print string representing the return value from
    :meth:`.decode`.
    """

    (fieldsDict, fieldsOrder) = decodeResults

    desc = ''
    for fieldName in fieldsOrder:
      (ranges, rangesStr) = fieldsDict[fieldName]
      if len(desc) > 0:
        desc += ", %s:" % (fieldName)
      else:
        desc += "%s:" % (fieldName)

      desc += "[%s]" % (rangesStr)

    return desc