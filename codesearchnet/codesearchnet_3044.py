def get(self):
    """ get method """
    try:
      cluster = self.get_argument_cluster()
      role = self.get_argument_role()
      environ = self.get_argument_environ()
      topology_name = self.get_argument_topology()
      component = self.get_argument_component()
      metric_names = self.get_required_arguments_metricnames()
      start_time = self.get_argument_starttime()
      end_time = self.get_argument_endtime()
      self.validateInterval(start_time, end_time)
      instances = self.get_arguments(constants.PARAM_INSTANCE)

      topology = self.tracker.getTopologyByClusterRoleEnvironAndName(
          cluster, role, environ, topology_name)
      metrics = yield tornado.gen.Task(metricstimeline.getMetricsTimeline,
                                       topology.tmaster, component, metric_names,
                                       instances, int(start_time), int(end_time))
      self.write_success_response(metrics)
    except Exception as e:
      Log.debug(traceback.format_exc())
      self.write_error_response(e)