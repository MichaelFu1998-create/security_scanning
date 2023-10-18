def register_metric(self, name, metric, time_bucket_in_sec):
    """Registers a given metric

    :param name: name of the metric
    :param metric: IMetric object to be registered
    :param time_bucket_in_sec: time interval for update to the metrics manager
    """
    if name in self.metrics_map:
      raise RuntimeError("Another metric has already been registered with name: %s" % name)

    Log.debug("Register metric: %s, with interval: %s", name, str(time_bucket_in_sec))
    self.metrics_map[name] = metric

    if time_bucket_in_sec in self.time_bucket_in_sec_to_metrics_name:
      self.time_bucket_in_sec_to_metrics_name[time_bucket_in_sec].append(name)
    else:
      self.time_bucket_in_sec_to_metrics_name[time_bucket_in_sec] = [name]
      self._register_timer_task(time_bucket_in_sec)