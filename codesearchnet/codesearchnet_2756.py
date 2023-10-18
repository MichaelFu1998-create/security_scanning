def get_comp_instance_metrics(cluster, environ, topology, component,
                              metrics, instances, time_range, role=None):
  '''
  Get the metrics for some instances of a topology from tracker
  :param cluster:
  :param environ:
  :param topology:
  :param component:
  :param metrics:     dict of display name to cuckoo name
  :param instances:
  :param time_range:  2-tuple consisting of start and end of range
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

  # form the fetch url
  request_url = tornado.httputil.url_concat(
      create_url(METRICS_URL_FMT), params)

  # convert a single instance to a list, if needed
  all_instances = instances if isinstance(instances, list) else [instances]

  # append each metric to the url
  for _, metric_name in metrics.items():
    request_url = tornado.httputil.url_concat(request_url, dict(metricname=metric_name[0]))

  # append each instance to the url
  for i in all_instances:
    request_url = tornado.httputil.url_concat(request_url, dict(instance=i))

  # append the time interval to the url
  request_url = tornado.httputil.url_concat(request_url, dict(interval=time_range[1]))

  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))