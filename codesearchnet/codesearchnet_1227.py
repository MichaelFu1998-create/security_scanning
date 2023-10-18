def getDict(self, encoderName, flattenedChosenValues):
    """ Return a dict that can be used to construct this encoder. This dict
    can be passed directly to the addMultipleEncoders() method of the
    multi encoder.

    Parameters:
    ----------------------------------------------------------------------
    encoderName:            name of the encoder
    flattenedChosenValues:  dict of the flattened permutation variables. Any
                              variables within this dict whose key starts
                              with encoderName will be substituted for
                              encoder constructor args which are being
                              permuted over.
    """
    encoder = dict(fieldname=self.fieldName,
                   name=self.name)

    # Get the position of each encoder argument
    for encoderArg, value in self.kwArgs.iteritems():
      # If a permuted variable, get its chosen value.
      if isinstance(value, PermuteVariable):
        value = flattenedChosenValues["%s:%s" % (encoderName, encoderArg)]

      encoder[encoderArg] = value

    # Special treatment for DateEncoder timeOfDay and dayOfWeek stuff. In the
    #  permutations file, the class can be one of:
    #    DateEncoder.timeOfDay
    #    DateEncoder.dayOfWeek
    #    DateEncoder.season
    # If one of these, we need to intelligently set the constructor args.
    if '.' in self.encoderClass:
      (encoder['type'], argName) = self.encoderClass.split('.')
      argValue = (encoder['w'], encoder['radius'])
      encoder[argName] = argValue
      encoder.pop('w')
      encoder.pop('radius')
    else:
      encoder['type'] = self.encoderClass

    return encoder