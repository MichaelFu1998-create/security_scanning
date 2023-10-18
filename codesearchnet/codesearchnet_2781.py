def get(self, cluster, environ, topology, comp_name):
    '''
    :param cluster:
    :param environ:
    :param topology:
    :param comp_name:
    :return:
    '''
    start_time = time.time()
    comp_names = []
    if comp_name == "All":
      lplan = yield access.get_logical_plan(cluster, environ, topology)
      if not lplan:
        self.write(dict())
        return

      if not 'spouts' in lplan or not 'bolts' in lplan:
        self.write(dict())
        return
      comp_names = lplan['spouts'].keys()
      comp_names.extend(lplan['bolts'].keys())
    else:
      comp_names = [comp_name]
    exception_infos = dict()
    for comp_name in comp_names:
      exception_infos[comp_name] = yield access.get_component_exceptionsummary(
          cluster, environ, topology, comp_name)

    # Combine exceptions from multiple component
    aggregate_exceptions = dict()
    for comp_name, exception_logs in exception_infos.items():
      for exception_log in exception_logs:
        class_name = exception_log['class_name']
        if class_name != '':
          if not class_name in aggregate_exceptions:
            aggregate_exceptions[class_name] = 0
          aggregate_exceptions[class_name] += int(exception_log['count'])
    # Put the exception value in a table
    aggregate_exceptions_table = []
    for key in aggregate_exceptions:
      aggregate_exceptions_table.append([key, str(aggregate_exceptions[key])])
    result = dict(
        status="success",
        executiontime=time.time() - start_time,
        result=aggregate_exceptions_table)
    self.write(result)