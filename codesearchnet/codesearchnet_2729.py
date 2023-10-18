def distribute_package(roles, cl_args):
  '''
  distribute Heron packages to all nodes
  '''
  Log.info("Distributing heron package to nodes (this might take a while)...")
  masters = roles[Role.MASTERS]
  slaves = roles[Role.SLAVES]

  tar_file = tempfile.NamedTemporaryFile(suffix=".tmp").name
  Log.debug("TAR file %s to %s" % (cl_args["heron_dir"], tar_file))
  make_tarfile(tar_file, cl_args["heron_dir"])
  dist_nodes = masters.union(slaves)

  scp_package(tar_file, dist_nodes, cl_args)