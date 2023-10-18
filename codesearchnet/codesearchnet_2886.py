def handle_assignment_msg(self, pplan):
    """Called when new NewInstanceAssignmentMessage arrives

    Tells this instance to become either spout/bolt.

    :param pplan: PhysicalPlan proto
    """

    new_helper = PhysicalPlanHelper(pplan, self.instance.instance_id,
                                    self.topo_pex_file_abs_path)
    if self.my_pplan_helper is not None and \
      (self.my_pplan_helper.my_component_name != new_helper.my_component_name or
       self.my_pplan_helper.my_task_id != new_helper.my_task_id):
      raise RuntimeError("Our Assignment has changed. We will die to pick it.")

    new_helper.set_topology_context(self.metrics_collector)

    if self.my_pplan_helper is None:
      Log.info("Received a new Physical Plan")
      Log.info("Push the new pplan_helper to Heron Instance")
      self._handle_assignment_msg(new_helper)
    else:
      Log.info("Received a new Physical Plan with the same assignment -- State Change")
      Log.info("Old state: %s, new state: %s.",
               self.my_pplan_helper.get_topology_state(), new_helper.get_topology_state())
      self._handle_state_change_msg(new_helper)