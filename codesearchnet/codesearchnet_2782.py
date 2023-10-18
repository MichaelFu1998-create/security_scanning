def get(self):
    '''
    :return:
    '''
    # get all the topologies from heron nest
    topologies = yield access.get_topologies_states()

    result = dict()

    # now convert some of the fields to be displayable
    for cluster, cluster_value in topologies.items():
      result[cluster] = dict()
      for environ, environ_value in cluster_value.items():
        result[cluster][environ] = dict()
        for topology, topology_value in environ_value.items():
          if "jobname" not in topology_value or topology_value["jobname"] is None:
            continue

          if "submission_time" in topology_value:
            topology_value["submission_time"] = topology_value["submission_time"]
          else:
            topology_value["submission_time"] = '-'

          result[cluster][environ][topology] = topology_value

    self.write(result)