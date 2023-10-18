def fetch(self, cluster, metric, topology, component, instance, timerange, environ=None):
    '''
    :param cluster:
    :param metric:
    :param topology:
    :param component:
    :param instance:
    :param timerange:
    :param environ:
    :return:
    '''
    components = [component] if component != "*" else (yield get_comps(cluster, environ, topology))

    futures = []
    for comp in components:
      query = self.get_query(metric, comp, instance)
      future = get_metrics(cluster, environ, topology, timerange, query)
      futures.append(future)

    results = yield futures

    timelines = []
    for result in results:
      timelines.extend(result["timeline"])

    result = self.get_metric_response(timerange, timelines, False)

    raise tornado.gen.Return(result)