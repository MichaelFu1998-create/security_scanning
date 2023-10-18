def _handle_state_change_msg(self, new_helper):
    """Called when state change is commanded by stream manager"""
    assert self.my_pplan_helper is not None
    assert self.my_instance is not None and self.my_instance.py_class is not None

    if self.my_pplan_helper.get_topology_state() != new_helper.get_topology_state():
      # handle state change
      # update the pplan_helper
      self.my_pplan_helper = new_helper
      if new_helper.is_topology_running():
        if not self.is_instance_started:
          self.start_instance_if_possible()
        self.my_instance.py_class.invoke_activate()
      elif new_helper.is_topology_paused():
        self.my_instance.py_class.invoke_deactivate()
      else:
        raise RuntimeError("Unexpected TopologyState update: %s" % new_helper.get_topology_state())
    else:
      Log.info("Topology state remains the same.")