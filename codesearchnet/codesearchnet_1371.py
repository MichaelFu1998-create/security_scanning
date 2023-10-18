def scalarsToStr(self, scalarValues, scalarNames=None):
    """
    Return a pretty print string representing the return values from
    :meth:`.getScalars` and :meth:`.getScalarNames`.

    :param scalarValues: input values to encode to string
    :param scalarNames: optional input of scalar names to convert. If None, gets
                       scalar names from :meth:`.getScalarNames`
    :return: string representation of scalar values
    """

    if scalarNames is None:
      scalarNames = self.getScalarNames()

    desc = ''
    for (name, value) in zip(scalarNames, scalarValues):
      if len(desc) > 0:
        desc += ", %s:%.2f" % (name, value)
      else:
        desc += "%s:%.2f" % (name, value)

    return desc