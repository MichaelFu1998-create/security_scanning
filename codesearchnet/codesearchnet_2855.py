def run(command, parser, cl_args, unknown_args):
  '''
  Submits the topology to the scheduler
    * Depending on the topology file name extension, we treat the file as a
      fatjar (if the ext is .jar) or a tar file (if the ext is .tar/.tar.gz).
    * We upload the topology file to the packer, update zookeeper and launch
      scheduler jobs representing that topology
    * You can see your topology in Heron UI
  :param command:
  :param parser:
  :param cl_args:
  :param unknown_args:
  :return:
  '''
  Log.debug("Submit Args %s", cl_args)

  # get the topology file name
  topology_file = cl_args['topology-file-name']

  if urlparse.urlparse(topology_file).scheme:
    cl_args['topology-file-name'] = download(topology_file, cl_args['cluster'])
    topology_file = cl_args['topology-file-name']
    Log.debug("download uri to local file: %s", topology_file)

  # check to see if the topology file exists
  if not os.path.isfile(topology_file):
    err_context = "Topology file '%s' does not exist" % topology_file
    return SimpleResult(Status.InvocationError, err_context)

  # check if it is a valid file type
  jar_type = topology_file.endswith(".jar")
  tar_type = topology_file.endswith(".tar") or topology_file.endswith(".tar.gz")
  pex_type = topology_file.endswith(".pex")
  cpp_type = topology_file.endswith(".dylib") or topology_file.endswith(".so")
  if not (jar_type or tar_type or pex_type or cpp_type):
    _, ext_name = os.path.splitext(topology_file)
    err_context = "Unknown file type '%s'. Please use .tar "\
                  "or .tar.gz or .jar or .pex or .dylib or .so file"\
                  % ext_name
    return SimpleResult(Status.InvocationError, err_context)

  # check if extra launch classpath is provided and if it is validate
  if cl_args['extra_launch_classpath']:
    valid_classpath = classpath.valid_java_classpath(cl_args['extra_launch_classpath'])
    if not valid_classpath:
      err_context = "One of jar or directory in extra launch classpath does not exist: %s" % \
        cl_args['extra_launch_classpath']
      return SimpleResult(Status.InvocationError, err_context)

  # create a temporary directory for topology definition file
  tmp_dir = tempfile.mkdtemp()
  opts.cleaned_up_files.append(tmp_dir)

  # if topology needs to be launched in deactivated state, do it so
  if cl_args['deploy_deactivated']:
    initial_state = topology_pb2.TopologyState.Name(topology_pb2.PAUSED)
  else:
    initial_state = topology_pb2.TopologyState.Name(topology_pb2.RUNNING)

  # set the tmp dir and deactivated state in global options
  opts.set_config('cmdline.topologydefn.tmpdirectory', tmp_dir)
  opts.set_config('cmdline.topology.initial.state', initial_state)
  opts.set_config('cmdline.topology.role', cl_args['role'])
  opts.set_config('cmdline.topology.environment', cl_args['environ'])

  # Use CLI release yaml file if the release_yaml_file config is empty
  if not cl_args['release_yaml_file']:
    cl_args['release_yaml_file'] = config.get_heron_release_file()

  # check the extension of the file name to see if it is tar/jar file.
  if jar_type:
    return submit_fatjar(cl_args, unknown_args, tmp_dir)
  elif tar_type:
    return submit_tar(cl_args, unknown_args, tmp_dir)
  elif cpp_type:
    return submit_cpp(cl_args, unknown_args, tmp_dir)
  else:
    return submit_pex(cl_args, unknown_args, tmp_dir)