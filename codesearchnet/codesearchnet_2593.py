def get(self):
    """ get method """
    try:
      cluster = self.get_argument_cluster()
      role = self.get_argument_role()
      environ = self.get_argument_environ()
      topology_name = self.get_argument_topology()
      instance = self.get_argument_instance()
      topology_info = self.tracker.getTopologyInfo(topology_name, cluster, role, environ)
      result = yield getInstancePid(topology_info, instance)
      self.write_success_response(result)
    except Exception as e:
      Log.debug(traceback.format_exc())
      self.write_error_response(e)