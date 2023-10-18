def get_execution_state(self, topologyName, callback=None):
    """
    Get execution state
    """
    if callback:
      self.execution_state_watchers[topologyName].append(callback)
    else:
      execution_state_path = self.get_execution_state_path(topologyName)
      with open(execution_state_path) as f:
        data = f.read()
        executionState = ExecutionState()
        executionState.ParseFromString(data)
        return executionState