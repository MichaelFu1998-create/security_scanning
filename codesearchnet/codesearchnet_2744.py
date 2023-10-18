def get(self):
    """ get method """
    # Get all the values for parameter "cluster".
    clusters = self.get_arguments(constants.PARAM_CLUSTER)
    # Get all the values for parameter "environ".
    environs = self.get_arguments(constants.PARAM_ENVIRON)
    # Get role
    role = self.get_argument_role()

    ret = {}
    topologies = self.tracker.topologies
    for topology in topologies:
      cluster = topology.cluster
      environ = topology.environ
      execution_state = topology.execution_state

      if not cluster or not execution_state or not environ:
        continue

      topo_role = execution_state.role
      if not topo_role:
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

      # This role is not asked for.
      # Note that "if not role", then
      # we show for all the roles.
      if role and role != topo_role:
        continue

      if cluster not in ret:
        ret[cluster] = {}
      if topo_role not in ret[cluster]:
        ret[cluster][topo_role] = {}
      if environ not in ret[cluster][topo_role]:
        ret[cluster][topo_role][environ] = []
      ret[cluster][topo_role][environ].append(topology.name)
    self.write_success_response(ret)