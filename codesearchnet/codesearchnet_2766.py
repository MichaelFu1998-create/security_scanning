def get_container_file_data(cluster, environ, topology, container,
                            path, offset, length, role=None):
  '''
  :param cluster:
  :param environ:
  :param topology:
  :param container:
  :param path:
  :param offset:
  :param length:
  :param role:
  :return:
  '''
  params = dict(
      cluster=cluster,
      environ=environ,
      topology=topology,
      container=container,
      path=path,
      offset=offset,
      length=length)

  if role is not None:
    params['role'] = role

  request_url = tornado.httputil.url_concat(
      create_url(FILE_DATA_URL_FMT), params)

  if role is not None:
    request_url = tornado.httputil.url_concat(request_url, dict(role=role))

  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))