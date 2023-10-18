def get_topology_config(self):
    """Returns the topology config"""
    if self.pplan.topology.HasField("topology_config"):
      return self._get_dict_from_config(self.pplan.topology.topology_config)
    else:
      return {}