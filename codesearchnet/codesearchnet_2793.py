def delete_topology_from_zk(self, topologyName):
    """
    Removes the topology entry from:
    1. topologies list,
    2. pplan,
    3. execution_state, and
    """
    self.delete_pplan(topologyName)
    self.delete_execution_state(topologyName)
    self.delete_topology(topologyName)