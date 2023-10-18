def __constructMetricsModules(self, metricSpecs):
    """
    Creates the required metrics modules

    Parameters:
    -----------------------------------------------------------------------
    metricSpecs:
      A sequence of MetricSpec objects that specify which metric modules to
      instantiate
    """
    if not metricSpecs:
      return

    self.__metricSpecs = metricSpecs
    for spec in metricSpecs:
      if not InferenceElement.validate(spec.inferenceElement):
        raise ValueError("Invalid inference element for metric spec: %r" %spec)

      self.__metrics.append(metrics.getModule(spec))
      self.__metricLabels.append(spec.getLabel())