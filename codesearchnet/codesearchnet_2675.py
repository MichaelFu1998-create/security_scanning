def _get_streaming_processes(self):
    '''
    Returns the processes to handle streams, including the stream-mgr and the user code containing
    the stream logic of the topology
    '''
    retval = {}
    instance_plans = self._get_instance_plans(self.packing_plan, self.shard)
    instance_info = []
    for instance_plan in instance_plans:
      global_task_id = instance_plan.task_id
      component_index = instance_plan.component_index
      component_name = instance_plan.component_name
      instance_id = "container_%s_%s_%d" % (str(self.shard), component_name, global_task_id)
      instance_info.append((instance_id, component_name, global_task_id, component_index))

    stmgr_cmd_lst = [
        self.stmgr_binary,
        '--topology_name=%s' % self.topology_name,
        '--topology_id=%s' % self.topology_id,
        '--topologydefn_file=%s' % self.topology_defn_file,
        '--zkhostportlist=%s' % self.state_manager_connection,
        '--zkroot=%s' % self.state_manager_root,
        '--stmgr_id=%s' % self.stmgr_ids[self.shard],
        '--instance_ids=%s' % ','.join(map(lambda x: x[0], instance_info)),
        '--myhost=%s' % self.master_host,
        '--data_port=%s' % str(self.master_port),
        '--local_data_port=%s' % str(self.tmaster_controller_port),
        '--metricsmgr_port=%s' % str(self.metrics_manager_port),
        '--shell_port=%s' % str(self.shell_port),
        '--config_file=%s' % self.heron_internals_config_file,
        '--override_config_file=%s' % self.override_config_file,
        '--ckptmgr_port=%s' % str(self.checkpoint_manager_port),
        '--ckptmgr_id=%s' % self.ckptmgr_ids[self.shard],
        '--metricscachemgr_mode=%s' % self.metricscache_manager_mode.lower()]

    stmgr_env = self.shell_env.copy() if self.shell_env is not None else {}
    stmgr_cmd = Command(stmgr_cmd_lst, stmgr_env)
    if os.environ.get('ENABLE_HEAPCHECK') is not None:
      stmgr_cmd.env.update({
          'LD_PRELOAD': "/usr/lib/libtcmalloc.so",
          'HEAPCHECK': "normal"
      })

    retval[self.stmgr_ids[self.shard]] = stmgr_cmd

    # metricsmgr_metrics_sink_config_file = 'metrics_sinks.yaml'

    retval[self.metricsmgr_ids[self.shard]] = self._get_metricsmgr_cmd(
        self.metricsmgr_ids[self.shard],
        self.metrics_sinks_config_file,
        self.metrics_manager_port
    )

    if self.is_stateful_topology:
      retval.update(self._get_ckptmgr_process())

    if self.pkg_type == 'jar' or self.pkg_type == 'tar':
      retval.update(self._get_java_instance_cmd(instance_info))
    elif self.pkg_type == 'pex':
      retval.update(self._get_python_instance_cmd(instance_info))
    elif self.pkg_type == 'so':
      retval.update(self._get_cpp_instance_cmd(instance_info))
    elif self.pkg_type == 'dylib':
      retval.update(self._get_cpp_instance_cmd(instance_info))
    else:
      raise ValueError("Unrecognized package type: %s" % self.pkg_type)

    return retval