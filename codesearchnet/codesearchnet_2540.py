def setTopologyInfo(self, topology):
    """
    Extracts info from the stored proto states and
    convert it into representation that is exposed using
    the API.
    This method is called on any change for the topology.
    For example, when a container moves and its host or some
    port changes. All the information is parsed all over
    again and cache is updated.
    """
    # Execution state is the most basic info.
    # If there is no execution state, just return
    # as the rest of the things don't matter.
    if not topology.execution_state:
      Log.info("No execution state found for: " + topology.name)
      return

    Log.info("Setting topology info for topology: " + topology.name)
    has_physical_plan = True
    if not topology.physical_plan:
      has_physical_plan = False

    Log.info("Setting topology info for topology: " + topology.name)
    has_packing_plan = True
    if not topology.packing_plan:
      has_packing_plan = False

    has_tmaster_location = True
    if not topology.tmaster:
      has_tmaster_location = False

    has_scheduler_location = True
    if not topology.scheduler_location:
      has_scheduler_location = False

    topologyInfo = {
        "name": topology.name,
        "id": topology.id,
        "logical_plan": None,
        "physical_plan": None,
        "packing_plan": None,
        "execution_state": None,
        "tmaster_location": None,
        "scheduler_location": None,
    }

    executionState = self.extract_execution_state(topology)
    executionState["has_physical_plan"] = has_physical_plan
    executionState["has_packing_plan"] = has_packing_plan
    executionState["has_tmaster_location"] = has_tmaster_location
    executionState["has_scheduler_location"] = has_scheduler_location
    executionState["status"] = topology.get_status()

    topologyInfo["metadata"] = self.extract_metadata(topology)
    topologyInfo["runtime_state"] = self.extract_runtime_state(topology)

    topologyInfo["execution_state"] = executionState
    topologyInfo["logical_plan"] = self.extract_logical_plan(topology)
    topologyInfo["physical_plan"] = self.extract_physical_plan(topology)
    topologyInfo["packing_plan"] = self.extract_packing_plan(topology)
    topologyInfo["tmaster_location"] = self.extract_tmaster(topology)
    topologyInfo["scheduler_location"] = self.extract_scheduler_location(topology)

    self.topologyInfos[(topology.name, topology.state_manager_name)] = topologyInfo