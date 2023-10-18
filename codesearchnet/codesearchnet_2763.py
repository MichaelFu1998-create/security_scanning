def get_instance_mem_histogram(cluster, environ, topology, instance, role=None):
  '''
  :param cluster:
  :param environ:
  :param topology:
  :param instance:
  :param role:
  :return:
  '''
  params = dict(
      cluster=cluster,
      environ=environ,
      topology=topology,
      instance=instance)

  if role is not None:
    params['role'] = role

  request_url = tornado.httputil.url_concat(
      create_url(HISTOGRAM_URL_FMT), params)

  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))