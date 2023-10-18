def get_scheduler_location(cluster, environ, topology, role=None):
  '''
  Get the scheduler location of a topology in a cluster from tracker
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
      create_url(SCHEDULER_LOCATION_URL_FMT), params)
  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))