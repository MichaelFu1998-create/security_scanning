def get(self):
    '''
    :return:
    '''
    cluster = self.get_argument("cluster")
    environ = self.get_argument("environ")
    topology = self.get_argument("topology")
    component = self.get_argument("component", default=None)
    metricnames = self.get_arguments("metricname")
    instances = self.get_arguments("instance")
    interval = self.get_argument("interval", default=-1)
    time_range = (0, interval)
    compnames = [component] if component else (yield access.get_comps(cluster, environ, topology))

    # fetch the metrics
    futures = {}
    for comp in compnames:
      future = access.get_comp_metrics(
          cluster, environ, topology, comp, instances,
          metricnames, time_range)
      futures[comp] = future

    results = yield futures

    self.write(results[component] if component else results)