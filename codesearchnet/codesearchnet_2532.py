def addNewTopology(self, state_manager, topologyName):
    """
    Adds a topology in the local cache, and sets a watch
    on any changes on the topology.
    """
    topology = Topology(topologyName, state_manager.name)
    Log.info("Adding new topology: %s, state_manager: %s",
             topologyName, state_manager.name)
    self.topologies.append(topology)

    # Register a watch on topology and change
    # the topologyInfo on any new change.
    topology.register_watch(self.setTopologyInfo)

    def on_topology_pplan(data):
      """watch physical plan"""
      Log.info("Watch triggered for topology pplan: " + topologyName)
      topology.set_physical_plan(data)
      if not data:
        Log.debug("No data to be set")

    def on_topology_packing_plan(data):
      """watch packing plan"""
      Log.info("Watch triggered for topology packing plan: " + topologyName)
      topology.set_packing_plan(data)
      if not data:
        Log.debug("No data to be set")

    def on_topology_execution_state(data):
      """watch execution state"""
      Log.info("Watch triggered for topology execution state: " + topologyName)
      topology.set_execution_state(data)
      if not data:
        Log.debug("No data to be set")

    def on_topology_tmaster(data):
      """set tmaster"""
      Log.info("Watch triggered for topology tmaster: " + topologyName)
      topology.set_tmaster(data)
      if not data:
        Log.debug("No data to be set")

    def on_topology_scheduler_location(data):
      """set scheduler location"""
      Log.info("Watch triggered for topology scheduler location: " + topologyName)
      topology.set_scheduler_location(data)
      if not data:
        Log.debug("No data to be set")

    # Set watches on the pplan, execution_state, tmaster and scheduler_location.
    state_manager.get_pplan(topologyName, on_topology_pplan)
    state_manager.get_packing_plan(topologyName, on_topology_packing_plan)
    state_manager.get_execution_state(topologyName, on_topology_execution_state)
    state_manager.get_tmaster(topologyName, on_topology_tmaster)
    state_manager.get_scheduler_location(topologyName, on_topology_scheduler_location)