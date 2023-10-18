def get_instances(cluster, environ, topology, role=None):
  '''
  Get the list of instances for the topology from Heron Nest
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
      create_url(PHYSICALPLAN_URL_FMT), params)
  pplan = yield fetch_url_as_json(request_url)
  instances = pplan['instances'].keys()
  raise tornado.gen.Return(instances)