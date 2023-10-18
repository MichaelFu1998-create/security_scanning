def get(self):
    """ get method """
    # Get all the values for parameter "cluster".
    clusters = self.get_arguments(constants.PARAM_CLUSTER)

    # Get all the values for parameter "environ".
    environs = self.get_arguments(constants.PARAM_ENVIRON)

    role = self.get_argument_role()

    ret = {}
    topologies = self.tracker.topologies
    for topology in topologies:
      cluster = topology.cluster
      environ = topology.environ
      if not cluster or not environ:
        continue

      # This cluster is not asked for.
      # Note that "if not clusters", then
      # we show for all the clusters.
      if clusters and cluster not in clusters:
        continue

      # This environ is not asked for.
      # Note that "if not environs", then
      # we show for all the environs.
      if environs and environ not in environs:
        continue

      if cluster not in ret:
        ret[cluster] = {}
      if environ not in ret[cluster]:
        ret[cluster][environ] = {}
      try:
        topology_info = self.tracker.getTopologyInfo(topology.name, cluster, role, environ)
        if topology_info and "execution_state" in topology_info:
          ret[cluster][environ][topology.name] = topology_info["execution_state"]
      except Exception:
        # Do nothing
        pass
    self.write_success_response(ret)