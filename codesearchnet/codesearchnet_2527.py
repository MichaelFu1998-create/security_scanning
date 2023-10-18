def get_status(self):
    """
    Get the current state of this topology.
    The state values are from the topology.proto
    RUNNING = 1, PAUSED = 2, KILLED = 3
    if the state is None "Unknown" is returned.
    """
    status = None
    if self.physical_plan and self.physical_plan.topology:
      status = self.physical_plan.topology.state

    if status == 1:
      return "Running"
    elif status == 2:
      return "Paused"
    elif status == 3:
      return "Killed"
    else:
      return "Unknown"