def get(self):
    """ get """
    try:
      cluster = self.get_argument_cluster()
      environ = self.get_argument_environ()
      role = self.get_argument_role()
      topology_name = self.get_argument_topology()
      component = self.get_argument_component()
      topology = self.tracker.getTopologyByClusterRoleEnvironAndName(
          cluster, role, environ, topology_name)
      instances = self.get_arguments(constants.PARAM_INSTANCE)
      exceptions_summary = yield tornado.gen.Task(self.getComponentExceptionSummary,
                                                  topology.tmaster, component, instances)
      self.write_success_response(exceptions_summary)
    except Exception as e:
      Log.debug(traceback.format_exc())
      self.write_error_response(e)