def sameTMParams(tp1, tp2):
  """Given two TM instances, see if any parameters are different."""
  result = True
  for param in ["numberOfCols", "cellsPerColumn", "initialPerm", "connectedPerm",
                "minThreshold", "newSynapseCount", "permanenceInc", "permanenceDec",
                "permanenceMax", "globalDecay", "activationThreshold",
                "doPooling", "segUpdateValidDuration",
                "burnIn", "pamLength", "maxAge"]:
    if getattr(tp1, param) != getattr(tp2,param):
      print param,"is different"
      print getattr(tp1, param), "vs", getattr(tp2,param)
      result = False
  return result