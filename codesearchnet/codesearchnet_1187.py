def requireAnomalyModel(func):
  """
  Decorator for functions that require anomaly models.
  """
  @wraps(func)
  def _decorator(self, *args, **kwargs):
    if not self.getInferenceType() == InferenceType.TemporalAnomaly:
      raise RuntimeError("Method required a TemporalAnomaly model.")
    if self._getAnomalyClassifier() is None:
      raise RuntimeError("Model does not support this command. Model must"
          "be an active anomalyDetector model.")
    return func(self, *args, **kwargs)
  return _decorator