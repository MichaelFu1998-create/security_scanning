def get_comps(cluster, environ, topology, role=None):
  '''
  Get the list of component names for the topology from Heron Nest
  :param cluster:
  :param environ:
  :param topology:
  :param role:
  :return:
  '''
  params = dict(cluster=cluster, environ=environ, topology=topology)
  if role is not None:
    params['role'] = role
  request_url = tornado.httputil.url_concat(
      create_url(LOGICALPLAN_URL_FMT), params)
  lplan = yield fetch_url_as_json(request_url)
  comps = lplan['spouts'].keys() + lplan['bolts'].keys()
  raise tornado.gen.Return(comps)