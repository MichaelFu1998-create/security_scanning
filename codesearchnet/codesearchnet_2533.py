def removeTopology(self, topology_name, state_manager_name):
    """
    Removes the topology from the local cache.
    """
    topologies = []
    for top in self.topologies:
      if (top.name == topology_name and
          top.state_manager_name == state_manager_name):
        # Remove topologyInfo
        if (topology_name, state_manager_name) in self.topologyInfos:
          self.topologyInfos.pop((topology_name, state_manager_name))
      else:
        topologies.append(top)

    self.topologies = topologies