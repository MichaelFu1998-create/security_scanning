def get(self):
    """ get method """
    try:
      cluster = self.get_argument_cluster()
      role = self.get_argument_role()
      environ = self.get_argument_environ()
      topology_name = self.get_argument_topology()
      topology_info = self.tracker.getTopologyInfo(topology_name, cluster, role, environ)
      runtime_state = topology_info["runtime_state"]
      runtime_state["topology_version"] = topology_info["metadata"]["release_version"]
      topology = self.tracker.getTopologyByClusterRoleEnvironAndName(
          cluster, role, environ, topology_name)
      reg_summary = yield tornado.gen.Task(self.getStmgrsRegSummary, topology.tmaster)
      for stmgr, reg in reg_summary.items():
        runtime_state["stmgrs"].setdefault(stmgr, {})["is_registered"] = reg
      self.write_success_response(runtime_state)
    except Exception as e:
      Log.debug(traceback.format_exc())
      self.write_error_response(e)