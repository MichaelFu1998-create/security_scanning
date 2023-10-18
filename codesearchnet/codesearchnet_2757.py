def get_comp_metrics(cluster, environ, topology, component,
                     instances, metricnames, time_range, role=None):
  '''
  Get the metrics for all the instances of a topology from Heron Nest
  :param cluster:
  :param environ:
  :param topology:
  :param component:
  :param instances:
  :param metricnames:   dict of display name to cuckoo name
  :param time_range:    2-tuple consisting of start and end of range
  :param role:
  :return:
  '''
  params = dict(
      cluster=cluster,
      environ=environ,
      topology=topology,
      component=component)
  if role is not None:
    params['role'] = role

  # form the url
  request_url = tornado.httputil.url_concat(
      create_url(METRICS_URL_FMT), params)

  # append each metric to the url
  for metric_name in metricnames:
    request_url = tornado.httputil.url_concat(request_url, dict(metricname=metric_name))

  # append each instance to the url
  for instance in instances:
    request_url = tornado.httputil.url_concat(request_url, dict(instance=instance))

  # append the time interval to the url
  request_url = tornado.httputil.url_concat(request_url, dict(interval=time_range[1]))

  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))