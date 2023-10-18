def update(self, results):
    """
    Compute the new metrics values, given the next inference/ground-truth values

    :param results: (:class:`~nupic.frameworks.opf.opf_utils.ModelResult`) 
           object that was computed during the last iteration of the model.

    :returns: (dict) where each key is the metric-name, and the values are
              it scalar value.

    """

    #print "\n\n---------------------------------------------------------------"
    #print "Model results: \nrawInput:%s \ninferences:%s" % \
    #      (pprint.pformat(results.rawInput), pprint.pformat(results.inferences))

    self._addResults(results)

    if  not self.__metricSpecs \
        or self.__currentInference is None:
      return {}

    metricResults = {}
    for metric, spec, label in zip(self.__metrics,
                                   self.__metricSpecs,
                                   self.__metricLabels):

      inferenceElement = spec.inferenceElement
      field = spec.field
      groundTruth = self._getGroundTruth(inferenceElement)
      inference = self._getInference(inferenceElement)
      rawRecord = self._getRawGroundTruth()
      result = self.__currentResult
      if field:
        if type(inference) in (list, tuple):
          if field in self.__fieldNameIndexMap:
            # NOTE: If the predicted field is not fed in at the bottom, we
            #  won't have it in our fieldNameIndexMap
            fieldIndex = self.__fieldNameIndexMap[field]
            inference = inference[fieldIndex]
          else:
            inference = None
        if groundTruth is not None:
          if type(groundTruth) in (list, tuple):
            if field in self.__fieldNameIndexMap:
              # NOTE: If the predicted field is not fed in at the bottom, we
              #  won't have it in our fieldNameIndexMap
              fieldIndex = self.__fieldNameIndexMap[field]
              groundTruth = groundTruth[fieldIndex]
            else:
              groundTruth = None
          else:
            # groundTruth could be a dict based off of field names
            groundTruth = groundTruth[field]

      metric.addInstance(groundTruth=groundTruth,
                         prediction=inference,
                         record=rawRecord,
                         result=result)

      metricResults[label] = metric.getMetric()['value']

    return metricResults