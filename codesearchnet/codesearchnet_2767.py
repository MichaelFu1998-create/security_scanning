def get_filestats(cluster, environ, topology, container, path, role=None):
  '''
  :param cluster:
  :param environ:
  :param topology:
  :param container:
  :param path:
  :param role:
  :return:
  '''
  params = dict(
      cluster=cluster,
      environ=environ,
      topology=topology,
      container=container,
      path=path)

  if role is not None:
    params['role'] = role

  request_url = tornado.httputil.url_concat(create_url(FILESTATS_URL_FMT), params)

  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))