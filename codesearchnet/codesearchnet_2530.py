def getTopologyByClusterRoleEnvironAndName(self, cluster, role, environ, topologyName):
    """
    Find and return the topology given its cluster, environ, topology name, and
    an optional role.
    Raises exception if topology is not found, or more than one are found.
    """
    topologies = list(filter(lambda t: t.name == topologyName
                             and t.cluster == cluster
                             and (not role or t.execution_state.role == role)
                             and t.environ == environ, self.topologies))
    if not topologies or len(topologies) > 1:
      if role is not None:
        raise Exception("Topology not found for {0}, {1}, {2}, {3}".format(
            cluster, role, environ, topologyName))
      else:
        raise Exception("Topology not found for {0}, {1}, {2}".format(
            cluster, environ, topologyName))

    # There is only one topology which is returned.
    return topologies[0]