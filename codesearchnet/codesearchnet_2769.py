def fetch_max(self, cluster, metric, topology, component, instance, timerange, environ=None):
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

    result = {}
    futures = []
    for comp in components:
      query = self.get_query(metric, comp, instance)
      max_query = "MAX(%s)" % query
      future = get_metrics(cluster, environ, topology, timerange, max_query)
      futures.append(future)

    results = yield futures

    data = self.compute_max(results)

    result = self.get_metric_response(timerange, data, True)

    raise tornado.gen.Return(result)