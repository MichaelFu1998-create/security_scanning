def getParamLabels(self):
    """
    Parameters:
    ----------------------------------------------------------------------
    retval:         a dictionary of model parameter labels. For each entry
                    the key is the name of the parameter and the value
                    is the value chosen for it.
    """
    params = self.__unwrapParams()

    # Hypersearch v2 stores the flattened parameter settings in "particleState"
    if "particleState" in params:
      retval = dict()
      queue = [(pair, retval) for pair in
               params["particleState"]["varStates"].iteritems()]
      while len(queue) > 0:
        pair, output = queue.pop()
        k, v = pair
        if ("position" in v and "bestPosition" in v and
            "velocity" in v):
          output[k] = v["position"]
        else:
          if k not in output:
            output[k] = dict()
          queue.extend((pair, output[k]) for pair in v.iteritems())
      return retval