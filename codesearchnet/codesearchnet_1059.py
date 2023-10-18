def _loadDummyModelParameters(self, params):
    """ Loads all the parameters for this dummy model. For any paramters
    specified as lists, read the appropriate value for this model using the model
    index """

    for key, value in params.iteritems():
      if type(value) == list:
        index = self.modelIndex % len(params[key])
        self._params[key] = params[key][index]
      else:
        self._params[key] = params[key]