def createEncoder():
  """
  Creates and returns a #MultiEncoder including a ScalarEncoder for
  energy consumption and a DateEncoder for the time of the day.

  @see nupic/encoders/__init__.py for type to file-name mapping
  @see nupic/encoders for encoder source files
  """
  encoder = MultiEncoder()
  encoder.addMultipleEncoders({
      "consumption": {"fieldname": u"consumption",
                      "type": "ScalarEncoder",
                      "name": u"consumption",
                      "minval": 0.0,
                      "maxval": 100.0,
                      "clipInput": True,
                      "w": 21,
                      "n": 500},
      "timestamp_timeOfDay": {"fieldname": u"timestamp",
                              "type": "DateEncoder",
                              "name": u"timestamp_timeOfDay",
                              "timeOfDay": (21, 9.5)}
  })
  return encoder