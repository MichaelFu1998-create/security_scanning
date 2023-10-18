def get_component_exceptions(cluster, environ, topology, component, role=None):
  '''
  Get exceptions for 'component' for 'topology'
  :param cluster:
  :param environ:
  :param topology:
  :param component:
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
  request_url = tornado.httputil.url_concat(
      create_url(EXCEPTIONS_URL_FMT), params)
  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))