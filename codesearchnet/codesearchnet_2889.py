def set_topology_context(self, metrics_collector):
    """Sets a new topology context"""
    Log.debug("Setting topology context")
    cluster_config = self.get_topology_config()
    cluster_config.update(self._get_dict_from_config(self.my_component.config))
    task_to_component_map = self._get_task_to_comp_map()
    self.context = TopologyContextImpl(cluster_config, self.pplan.topology, task_to_component_map,
                                       self.my_task_id, metrics_collector,
                                       self.topology_pex_abs_path)