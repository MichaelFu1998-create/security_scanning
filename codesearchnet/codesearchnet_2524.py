def set_execution_state(self, execution_state):
    """ set exectuion state """
    if not execution_state:
      self.execution_state = None
      self.cluster = None
      self.environ = None
    else:
      self.execution_state = execution_state
      cluster, environ = self.get_execution_state_dc_environ(execution_state)
      self.cluster = cluster
      self.environ = environ
      self.zone = cluster
    self.trigger_watches()