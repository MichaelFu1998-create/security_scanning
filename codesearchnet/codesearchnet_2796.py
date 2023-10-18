def get_topology(self, topologyName, callback=None):
    """get topology"""
    if callback:
      self.topology_watchers[topologyName].append(callback)
    else:
      topology_path = self.get_topology_path(topologyName)
      with open(topology_path) as f:
        data = f.read()
        topology = Topology()
        topology.ParseFromString(data)
        return topology