def update_reduced_metric(self, name, value, key=None):
    """Update the value of ReducedMetric or MultiReducedMetric

    :type name: str
    :param name: name of the registered metric to be updated.
    :param value: specifies a value to be reduced.
    :type key: str or None
    :param key: specifies a key for MultiReducedMetric. Needs to be `None` for updating
                ReducedMetric.
    """
    if name not in self.metrics:
      Log.error("In update_reduced_metric(): %s is not registered in the metric", name)

    if key is None and isinstance(self.metrics[name], ReducedMetric):
      self.metrics[name].update(value)
    elif key is not None and isinstance(self.metrics[name], MultiReducedMetric):
      self.metrics[name].update(key, value)
    else:
      Log.error("In update_count(): %s is registered but not supported with this method", name)