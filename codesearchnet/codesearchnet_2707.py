def get(self):
    """ get method """
    try:
      cluster = self.get_argument_cluster()

      role = self.get_argument_role()
      environ = self.get_argument_environ()
      topology_name = self.get_argument_topology()
      topology = self.tracker.getTopologyByClusterRoleEnvironAndName(
          cluster, role, environ, topology_name)

      start_time = self.get_argument_starttime()
      end_time = self.get_argument_endtime()
      self.validateInterval(start_time, end_time)

      query = self.get_argument_query()
      metrics = yield tornado.gen.Task(self.executeMetricsQuery,
                                       topology.tmaster, query, int(start_time), int(end_time))
      self.write_success_response(metrics)
    except Exception as e:
      Log.debug(traceback.format_exc())
      self.write_error_response(e)