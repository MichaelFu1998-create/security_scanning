def getTopologyInfo(self, topologyName, cluster, role, environ):
    """
    Returns the JSON representation of a topology
    by its name, cluster, environ, and an optional role parameter.
    Raises exception if no such topology is found.
    """
    # Iterate over the values to filter the desired topology.
    for (topology_name, _), topologyInfo in self.topologyInfos.items():
      executionState = topologyInfo["execution_state"]
      if (topologyName == topology_name and
          cluster == executionState["cluster"] and
          environ == executionState["environ"]):
        # If role is specified, first try to match "role" field. If "role" field
        # does not exist, try to match "submission_user" field.
        if not role or executionState.get("role") == role:
          return topologyInfo
    if role is not None:
      Log.info("Could not find topology info for topology: %s," \
               "cluster: %s, role: %s, and environ: %s",
               topologyName, cluster, role, environ)
    else:
      Log.info("Could not find topology info for topology: %s," \
               "cluster: %s and environ: %s", topologyName, cluster, environ)
    raise Exception("No topology found")