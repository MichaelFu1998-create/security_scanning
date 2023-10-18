def getModelDescription(self):
    """
    Parameters:
    ----------------------------------------------------------------------
    retval:         Printable description of the model.
    """
    params = self.__unwrapParams()

    if "experimentName" in params:
      return params["experimentName"]

    else:
      paramSettings = self.getParamLabels()
      # Form a csv friendly string representation of this model
      items = []
      for key, value in paramSettings.items():
        items.append("%s_%s" % (key, value))
      return ".".join(items)