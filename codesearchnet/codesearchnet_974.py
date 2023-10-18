def _generatePermEncoderStr(options, encoderDict):
  """ Generate the string that defines the permutations to apply for a given
  encoder.

  Parameters:
  -----------------------------------------------------------------------
  options: experiment params
  encoderDict: the encoder dict, which gets placed into the description.py


  For example, if the encoderDict contains:
      'consumption':     {
                'clipInput': True,
                'fieldname': u'consumption',
                'n': 100,
                'name': u'consumption',
                'type': 'AdaptiveScalarEncoder',
                'w': 21},

  The return string will contain:
    "PermuteEncoder(fieldName='consumption',
                    encoderClass='AdaptiveScalarEncoder',
                    w=21,
                    n=PermuteInt(28, 521),
                    clipInput=True)"

  """

  permStr = ""


  # If it's the encoder for the classifier input, then it's always present so
  # put it in as a dict in the permutations.py file instead of a
  # PermuteEncoder().
  if encoderDict.get('classifierOnly', False):
    permStr = "dict("
    for key, value in encoderDict.items():
      if key == "name":
        continue

      if key == 'n' and encoderDict['type'] != 'SDRCategoryEncoder':
        permStr += "n=PermuteInt(%d, %d), " % (encoderDict["w"] + 7,
                                               encoderDict["w"] + 500)
      else:
        if issubclass(type(value), basestring):
          permStr += "%s='%s', " % (key, value)
        else:
          permStr += "%s=%s, " % (key, value)
    permStr += ")"


  else:
    # Scalar encoders
    if encoderDict["type"] in ["ScalarSpaceEncoder", "AdaptiveScalarEncoder",
                             "ScalarEncoder", "LogEncoder"]:
      permStr = "PermuteEncoder("
      for key, value in encoderDict.items():
        if key == "fieldname":
          key = "fieldName"
        elif key == "type":
          key = "encoderClass"
        elif key == "name":
          continue

        if key == "n":
          permStr += "n=PermuteInt(%d, %d), " % (encoderDict["w"] + 1,
                                                 encoderDict["w"] + 500)
        elif key == "runDelta":
          if value and not "space" in encoderDict:
            permStr += "space=PermuteChoices([%s,%s]), " \
                     % (_quoteAndEscape("delta"), _quoteAndEscape("absolute"))
          encoderDict.pop("runDelta")

        else:
          if issubclass(type(value), basestring):
            permStr += "%s='%s', " % (key, value)
          else:
            permStr += "%s=%s, " % (key, value)
      permStr += ")"

    # Category encoder
    elif encoderDict["type"] in ["SDRCategoryEncoder"]:
      permStr = "PermuteEncoder("
      for key, value in encoderDict.items():
        if key == "fieldname":
          key = "fieldName"
        elif key == "type":
          key = "encoderClass"
        elif key == "name":
          continue

        if issubclass(type(value), basestring):
          permStr += "%s='%s', " % (key, value)
        else:
          permStr += "%s=%s, " % (key, value)
      permStr += ")"


    # Datetime encoder
    elif encoderDict["type"] in ["DateEncoder"]:
      permStr = "PermuteEncoder("
      for key, value in encoderDict.items():
        if key == "fieldname":
          key = "fieldName"
        elif key == "type":
          continue
        elif key == "name":
          continue

        if key == "timeOfDay":
          permStr += "encoderClass='%s.timeOfDay', " % (encoderDict["type"])
          permStr += "radius=PermuteFloat(0.5, 12), "
          permStr += "w=%d, " % (value[0])
        elif key == "dayOfWeek":
          permStr += "encoderClass='%s.dayOfWeek', " % (encoderDict["type"])
          permStr += "radius=PermuteFloat(1, 6), "
          permStr += "w=%d, " % (value[0])
        elif key == "weekend":
          permStr += "encoderClass='%s.weekend', " % (encoderDict["type"])
          permStr += "radius=PermuteChoices([1]),  "
          permStr += "w=%d, " % (value)
        else:
          if issubclass(type(value), basestring):
            permStr += "%s='%s', " % (key, value)
          else:
            permStr += "%s=%s, " % (key, value)
      permStr += ")"

    else:
      raise RuntimeError("Unsupported encoder type '%s'" % \
                          (encoderDict["type"]))

  return permStr