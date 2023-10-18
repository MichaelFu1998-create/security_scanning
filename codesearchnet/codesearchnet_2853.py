def submit_fatjar(cl_args, unknown_args, tmp_dir):
  '''
  We use the packer to make a package for the jar and dump it
  to a well-known location. We then run the main method of class
  with the specified arguments. We pass arguments as an environment variable HERON_OPTIONS.

  This will run the jar file with the topology_class_name. The submitter
  inside will write out the topology defn file to a location that
  we specify. Then we write the topology defn file to a well known
  location. We then write to appropriate places in zookeeper
  and launch the scheduler jobs
  :param cl_args:
  :param unknown_args:
  :param tmp_dir:
  :return:
  '''
  # execute main of the topology to create the topology definition
  topology_file = cl_args['topology-file-name']

  main_class = cl_args['topology-class-name']

  res = execute.heron_class(
      class_name=main_class,
      lib_jars=config.get_heron_libs(jars.topology_jars()),
      extra_jars=[topology_file],
      args=tuple(unknown_args),
      java_defines=cl_args['topology_main_jvm_property'])

  result.render(res)

  if not result.is_successful(res):
    err_context = ("Failed to create topology definition " \
      "file when executing class '%s' of file '%s'") % (main_class, topology_file)
    res.add_context(err_context)
    return res

  results = launch_topologies(cl_args, topology_file, tmp_dir)

  return results