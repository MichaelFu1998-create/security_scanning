def launch_topologies(cl_args, topology_file, tmp_dir):
  '''
  Launch topologies
  :param cl_args:
  :param topology_file:
  :param tmp_dir:
  :return: list(Responses)
  '''
  # the submitter would have written the .defn file to the tmp_dir
  defn_files = glob.glob(tmp_dir + '/*.defn')

  if len(defn_files) == 0:
    return SimpleResult(Status.HeronError, "No topologies found under %s" % tmp_dir)

  results = []
  for defn_file in defn_files:
    # load the topology definition from the file
    topology_defn = topology_pb2.Topology()
    try:
      handle = open(defn_file, "rb")
      topology_defn.ParseFromString(handle.read())
      handle.close()
    except Exception as e:
      err_context = "Cannot load topology definition '%s': %s" % (defn_file, e)
      return SimpleResult(Status.HeronError, err_context)

    # launch the topology
    Log.info("Launching topology: \'%s\'%s", topology_defn.name, launch_mode_msg(cl_args))

    # check if we have to do server or direct based deployment
    if cl_args['deploy_mode'] == config.SERVER_MODE:
      res = launch_topology_server(
          cl_args, topology_file, defn_file, topology_defn.name)
    else:
      res = launch_a_topology(
          cl_args, tmp_dir, topology_file, defn_file, topology_defn.name)
    results.append(res)

  return results