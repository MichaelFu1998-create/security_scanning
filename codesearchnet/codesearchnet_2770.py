def fetch_backpressure(self, cluster, metric, topology, component, instance, \
    timerange, is_max, environ=None):
    '''
    :param cluster:
    :param metric:
    :param topology:
    :param component:
    :param instance:
    :param timerange:
    :param isMax:
    :param environ:
    :return:
    '''
    instances = yield get_instances(cluster, environ, topology)
    if component != "*":
      filtered_inst = [instance for instance in instances if instance.split("_")[2] == component]
    else:
      filtered_inst = instances

    futures_dict = {}
    for inst in filtered_inst:
      query = queries.get(metric).format(inst)
      futures_dict[inst] = get_metrics(cluster, environ, topology, timerange, query)

    res = yield futures_dict

    if not is_max:
      timelines = []
      for key in res:
        result = res[key]
        # Replacing stream manager instance name with component instance name
        if len(result["timeline"]) > 0:
          result["timeline"][0]["instance"] = key
        timelines.extend(result["timeline"])
      result = self.get_metric_response(timerange, timelines, is_max)
    else:
      data = self.compute_max(res.values())
      result = self.get_metric_response(timerange, data, is_max)

    raise tornado.gen.Return(result)