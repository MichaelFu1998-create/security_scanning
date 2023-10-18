def get_container_file_download_url(cluster, environ, topology, container,
                                    path, role=None):
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

  request_url = tornado.httputil.url_concat(
      create_url(FILE_DOWNLOAD_URL_FMT), params)

  if role is not None:
    request_url = tornado.httputil.url_concat(request_url, dict(role=role))
  return request_url