def submit_tar(cl_args, unknown_args, tmp_dir):
  '''
  Extract and execute the java files inside the tar and then add topology
  definition file created by running submitTopology

  We use the packer to make a package for the tar and dump it
  to a well-known location. We then run the main method of class
  with the specified arguments. We pass arguments as an environment variable HERON_OPTIONS.
  This will run the jar file with the topology class name.

  The submitter inside will write out the topology defn file to a location
  that we specify. Then we write the topology defn file to a well known
  packer location. We then write to appropriate places in zookeeper
  and launch the aurora jobs
  :param cl_args:
  :param unknown_args:
  :param tmp_dir:
  :return:
  '''
  # execute main of the topology to create the topology definition
  topology_file = cl_args['topology-file-name']
  java_defines = cl_args['topology_main_jvm_property']
  main_class = cl_args['topology-class-name']
  res = execute.heron_tar(
      main_class,
      topology_file,
      tuple(unknown_args),
      tmp_dir,
      java_defines)

  result.render(res)

  if not result.is_successful(res):
    err_context = ("Failed to create topology definition " \
      "file when executing class '%s' of file '%s'") % (main_class, topology_file)
    res.add_context(err_context)
    return res

  return launch_topologies(cl_args, topology_file, tmp_dir)