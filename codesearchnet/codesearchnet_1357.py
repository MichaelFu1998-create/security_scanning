def getLabel(self, inferenceType=None):
    """ 
    Helper method that generates a unique label for a :class:`MetricSpec` / 
    :class:`~nupic.frameworks.opf.opf_utils.InferenceType` pair. The label is 
    formatted as follows:

    ::
        
        <predictionKind>:<metric type>:(paramName=value)*:field=<fieldname>

    For example:
    
    :: 
    
        classification:aae:paramA=10.2:paramB=20:window=100:field=pounds
    
    :returns: (string) label for inference type
    """
    result = []
    if inferenceType is not None:
      result.append(InferenceType.getLabel(inferenceType))
    result.append(self.inferenceElement)
    result.append(self.metric)

    params = self.params
    if params is not None:

      sortedParams= params.keys()
      sortedParams.sort()
      for param in sortedParams:
        # Don't include the customFuncSource - it is too long an unwieldy
        if param in ('customFuncSource', 'customFuncDef', 'customExpr'):
          continue
        value = params[param]
        if isinstance(value, str):
          result.extend(["%s='%s'"% (param, value)])
        else:
          result.extend(["%s=%s"% (param, value)])

    if self.field:
      result.append("field=%s"% (self.field) )

    return self._LABEL_SEPARATOR.join(result)