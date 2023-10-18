def getOutputElementCount(self, name):
    """
    Computes the width of dataOut.

    Overrides 
    :meth:`nupic.bindings.regions.PyRegion.PyRegion.getOutputElementCount`.
    """

    if name == "resetOut":
      print ("WARNING: getOutputElementCount should not have been called with "
             "resetOut")
      return 1

    elif name == "sequenceIdOut":
      print ("WARNING: getOutputElementCount should not have been called with "
             "sequenceIdOut")
      return 1

    elif name == "dataOut":
      if self.encoder is None:
        raise Exception("NuPIC requested output element count for 'dataOut' "
                        "on a RecordSensor node, but the encoder has not "
                        "been set")
      return self.encoder.getWidth()

    elif name == "sourceOut":
      if self.encoder is None:
        raise Exception("NuPIC requested output element count for 'sourceOut' "
                        "on a RecordSensor node, "
                        "but the encoder has not been set")
      return len(self.encoder.getDescription())

    elif name == "bucketIdxOut":
      return 1

    elif name == "actValueOut":
      return 1

    elif name == "categoryOut":
      return self.numCategories

    elif name == 'spatialTopDownOut' or name == 'temporalTopDownOut':
      if self.encoder is None:
        raise Exception("NuPIC requested output element count for 'sourceOut' "
                        "on a RecordSensor node, "
                        "but the encoder has not been set")
      return len(self.encoder.getDescription())
    else:
      raise Exception("Unknown output %s" % name)