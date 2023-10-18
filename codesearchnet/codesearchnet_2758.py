def get_metrics(cluster, environment, topology, timerange, query, role=None):
  '''
  Get the metrics for a topology from tracker
  :param cluster:
  :param environment:
  :param topology:
  :param timerange:
  :param query:
  :param role:
  :return:
  '''
  params = dict(
      cluster=cluster,
      environ=environment,
      topology=topology,
      starttime=timerange[0],
      endtime=timerange[1],
      query=query)

  if role is not None:
    params['role'] = role

  request_url = tornado.httputil.url_concat(
      create_url(METRICS_QUERY_URL_FMT), params
  )

  logging.info("get_metrics %s", request_url)
  raise tornado.gen.Return((yield fetch_url_as_json(request_url)))