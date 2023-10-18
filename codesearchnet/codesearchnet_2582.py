def get(self):
    '''
    :return:
    '''
    cluster = self.get_argument("cluster")
    environ = self.get_argument("environ")
    topology = self.get_argument("topology")
    component = self.get_argument("component", default=None)
    metric = self.get_argument("metric")
    instances = self.get_argument("instance")
    start = self.get_argument("starttime")
    end = self.get_argument("endtime")
    maxquery = self.get_argument("max", default=False)
    timerange = (start, end)
    compnames = [component]

    # fetch the metrics
    futures = {}
    if metric == "backpressure":
      for comp in compnames:
        future = query_handler.fetch_backpressure(cluster, metric, topology, component,
                                                  instances, timerange, maxquery, environ)
        futures[comp] = future
    else:
      fetch = query_handler.fetch_max if maxquery else query_handler.fetch
      for comp in compnames:
        future = fetch(cluster, metric, topology, component,
                       instances, timerange, environ)
        futures[comp] = future

    results = yield futures
    self.write(results[component] if component else results)