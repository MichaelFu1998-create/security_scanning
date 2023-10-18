def run_instance_jmap(cluster, environ, topology, instance, role=None):
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
      create_url(JMAP_URL_FMT), params)

  if role is not None:
    request_url = tornado.httputil.url_concat(request_url, dict(role=role))

  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))