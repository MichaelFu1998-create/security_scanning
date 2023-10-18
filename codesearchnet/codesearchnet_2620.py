def run_direct(command, cl_args, action, extra_args=[], extra_lib_jars=[]):
  '''
  helper function to take action on topologies
  :param command:
  :param cl_args:
  :param action:        description of action taken
  :return:
  '''
  topology_name = cl_args['topology-name']

  new_args = [
      "--cluster", cl_args['cluster'],
      "--role", cl_args['role'],
      "--environment", cl_args['environ'],
      "--submit_user", cl_args['submit_user'],
      "--heron_home", config.get_heron_dir(),
      "--config_path", cl_args['config_path'],
      "--override_config_file", cl_args['override_config_file'],
      "--release_file", config.get_heron_release_file(),
      "--topology_name", topology_name,
      "--command", command,
  ]
  new_args += extra_args
  lib_jars = config.get_heron_libs(jars.scheduler_jars() + jars.statemgr_jars())
  lib_jars += extra_lib_jars

  if Log.getEffectiveLevel() == logging.DEBUG:
    new_args.append("--verbose")

  # invoke the runtime manager to kill the topology
  result = execute.heron_class(
      'org.apache.heron.scheduler.RuntimeManagerMain',
      lib_jars,
      extra_jars=[],
      args=new_args
  )

  err_msg = "Failed to %s: %s" % (action, topology_name)
  succ_msg = "Successfully %s: %s" % (action, topology_name)
  result.add_context(err_msg, succ_msg)
  return result