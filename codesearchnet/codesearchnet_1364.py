def getScalarNames(self, parentFieldName=''):
    """
    Return the field names for each of the scalar values returned by
    getScalars.

    :param parentFieldName: The name of the encoder which is our parent. This
        name is prefixed to each of the field names within this encoder to
        form the keys of the dict() in the retval.

    :return: array of field names
    """
    names = []

    if self.encoders is not None:
      for (name, encoder, offset) in self.encoders:
        subNames = encoder.getScalarNames(parentFieldName=name)
        if parentFieldName != '':
          subNames = ['%s.%s' % (parentFieldName, name) for name in subNames]
        names.extend(subNames)
    else:
      if parentFieldName != '':
        names.append(parentFieldName)
      else:
        names.append(self.name)

    return names