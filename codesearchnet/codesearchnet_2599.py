def update_count(self, name, incr_by=1, key=None):
    """Update the value of CountMetric or MultiCountMetric

    :type name: str
    :param name: name of the registered metric to be updated.
    :type incr_by: int
    :param incr_by: specifies how much to increment. Default is 1.
    :type key: str or None
    :param key: specifies a key for MultiCountMetric. Needs to be `None` for updating CountMetric.
    """
    if name not in self.metrics:
      Log.error("In update_count(): %s is not registered in the metric", name)

    if key is None and isinstance(self.metrics[name], CountMetric):
      self.metrics[name].incr(incr_by)
    elif key is not None and isinstance(self.metrics[name], MultiCountMetric):
      self.metrics[name].incr(key, incr_by)
    else:
      Log.error("In update_count(): %s is registered but not supported with this method", name)