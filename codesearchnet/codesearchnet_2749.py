def get_logical_plan(cluster, environ, topology, role=None):
  '''
  Get the logical plan state of a topology in a cluster
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
  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))