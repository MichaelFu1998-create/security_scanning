def get(self):
    """ get method """
    try:
      cluster = self.get_argument_cluster()
      role = self.get_argument_role()
      environ = self.get_argument_environ()
      topology_name = self.get_argument_topology()
      component = self.get_argument_component()
      metric_names = self.get_required_arguments_metricnames()

      topology = self.tracker.getTopologyByClusterRoleEnvironAndName(
          cluster, role, environ, topology_name)

      interval = int(self.get_argument(constants.PARAM_INTERVAL, default=-1))
      instances = self.get_arguments(constants.PARAM_INSTANCE)

      metrics = yield tornado.gen.Task(
          self.getComponentMetrics,
          topology.tmaster, component, metric_names, instances, interval)

      self.write_success_response(metrics)
    except Exception as e:
      Log.debug(traceback.format_exc())
      self.write_error_response(e)