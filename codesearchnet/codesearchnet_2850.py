def launch_a_topology(cl_args, tmp_dir, topology_file, topology_defn_file, topology_name):
  '''
  Launch a topology given topology jar, its definition file and configurations
  :param cl_args:
  :param tmp_dir:
  :param topology_file:
  :param topology_defn_file:
  :param topology_name:
  :return:
  '''
  # get the normalized path for topology.tar.gz
  topology_pkg_path = config.normalized_class_path(os.path.join(tmp_dir, 'topology.tar.gz'))

  # get the release yaml file
  release_yaml_file = cl_args['release_yaml_file']

  # create a tar package with the cluster configuration and generated config files
  config_path = cl_args['config_path']
  tar_pkg_files = [topology_file, topology_defn_file]
  generated_config_files = [release_yaml_file, cl_args['override_config_file']]

  config.create_tar(topology_pkg_path, tar_pkg_files, config_path, generated_config_files)

  # pass the args to submitter main
  args = [
      "--cluster", cl_args['cluster'],
      "--role", cl_args['role'],
      "--environment", cl_args['environ'],
      "--submit_user", cl_args['submit_user'],
      "--heron_home", config.get_heron_dir(),
      "--config_path", config_path,
      "--override_config_file", cl_args['override_config_file'],
      "--release_file", release_yaml_file,
      "--topology_package", topology_pkg_path,
      "--topology_defn", topology_defn_file,
      "--topology_bin", os.path.basename(topology_file)   # pex/cpp file if pex/cpp specified
  ]

  if Log.getEffectiveLevel() == logging.DEBUG:
    args.append("--verbose")

  if cl_args["dry_run"]:
    args.append("--dry_run")
    if "dry_run_format" in cl_args:
      args += ["--dry_run_format", cl_args["dry_run_format"]]

  lib_jars = config.get_heron_libs(
      jars.scheduler_jars() + jars.uploader_jars() + jars.statemgr_jars() + jars.packing_jars()
  )
  extra_jars = cl_args['extra_launch_classpath'].split(':')

  # invoke the submitter to submit and launch the topology
  main_class = 'org.apache.heron.scheduler.SubmitterMain'
  res = execute.heron_class(
      class_name=main_class,
      lib_jars=lib_jars,
      extra_jars=extra_jars,
      args=args,
      java_defines=[])

  err_ctxt = "Failed to launch topology '%s' %s" % (topology_name, launch_mode_msg(cl_args))
  succ_ctxt = "Successfully launched topology '%s' %s" % (topology_name, launch_mode_msg(cl_args))

  res.add_context(err_ctxt, succ_ctxt)
  return res