def _fixupRandomEncoderParams(params, minVal, maxVal, minResolution):
  """
  Given model params, figure out the correct parameters for the
  RandomDistributed encoder. Modifies params in place.
  """
  encodersDict = (
    params["modelConfig"]["modelParams"]["sensorParams"]["encoders"]
  )

  for encoder in encodersDict.itervalues():
    if encoder is not None:
      if encoder["type"] == "RandomDistributedScalarEncoder":
        resolution = max(minResolution,
                         (maxVal - minVal) / encoder.pop("numBuckets")
                        )
        encodersDict["c1"]["resolution"] = resolution