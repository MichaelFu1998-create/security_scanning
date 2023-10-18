def _getMetrics(self):
    """ Protected function that can be overridden by subclasses. Its main purpose
    is to allow the the OPFDummyModelRunner to override this with deterministic
    values

    Returns: All the metrics being computed for this model
    """
    metric = None
    if self.metrics is not None:
      metric = self.metrics(self._currentRecordIndex+1)
    elif self.metricValue is not None:
      metric = self.metricValue
    else:
      raise RuntimeError('No metrics or metric value specified for dummy model')

    return {self._optimizeKeyPattern:metric}