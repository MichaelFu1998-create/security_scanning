def get_topology_info(cluster, environ, topology, role=None):
  '''
  :param cluster:
  :param environ:
  :param topology:
  :param role:
  :return:
  '''
  params = dict(
      cluster=cluster,
      environ=environ,
      topology=topology)

  if role is not None:
    params['role'] = role

  request_url = tornado.httputil.url_concat(create_url(INFO_URL_FMT), params)

  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))