def getScalarNames(self, parentFieldName=''):
    """ See method description in base.py """

    names = []

    # This forms a name which is the concatenation of the parentFieldName
    #   passed in and the encoder's own name.
    def _formFieldName(encoder):
      if parentFieldName == '':
        return encoder.name
      else:
        return '%s.%s' % (parentFieldName, encoder.name)

    # -------------------------------------------------------------------------
    # Get the scalar values for each sub-field
    if self.seasonEncoder is not None:
      names.append(_formFieldName(self.seasonEncoder))

    if self.dayOfWeekEncoder is not None:
      names.append(_formFieldName(self.dayOfWeekEncoder))

    if self.customDaysEncoder is not None:
      names.append(_formFieldName(self.customDaysEncoder))

    if self.weekendEncoder is not None:
      names.append(_formFieldName(self.weekendEncoder))

    if self.holidayEncoder is not None:
      names.append(_formFieldName(self.holidayEncoder))

    if self.timeOfDayEncoder is not None:
      names.append(_formFieldName(self.timeOfDayEncoder))

    return names