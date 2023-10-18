def args_to_job_params(envs, labels, inputs, inputs_recursive, outputs,
                       outputs_recursive, mounts, input_file_param_util,
                       output_file_param_util, mount_param_util):
  """Parse env, input, and output parameters into a job parameters and data.

  Passing arguments on the command-line allows for launching a single job.
  The env, input, and output arguments encode both the definition of the
  job as well as the single job's values.

  Env arguments are simple name=value pairs.
  Input and output file arguments can contain name=value pairs or just values.
  Either of the following is valid:

    uri
    myfile=uri

  Args:
    envs: list of environment variable job parameters
    labels: list of labels to attach to the tasks
    inputs: list of file input parameters
    inputs_recursive: list of recursive directory input parameters
    outputs: list of file output parameters
    outputs_recursive: list of recursive directory output parameters
    mounts: list of gcs buckets to mount
    input_file_param_util: Utility for producing InputFileParam objects.
    output_file_param_util: Utility for producing OutputFileParam objects.
    mount_param_util: Utility for producing MountParam objects.

  Returns:
    job_params: a dictionary of 'envs', 'inputs', and 'outputs' that defines the
    set of parameters and data for a job.
  """
  # Parse environmental variables and labels.
  env_data = parse_pair_args(envs, job_model.EnvParam)
  label_data = parse_pair_args(labels, job_model.LabelParam)

  # For input files, we need to:
  #   * split the input into name=uri pairs (name optional)
  #   * get the environmental variable name, or automatically set if null.
  #   * create the input file param
  input_data = set()
  for (recursive, args) in ((False, inputs), (True, inputs_recursive)):
    for arg in args:
      name, value = split_pair(arg, '=', nullable_idx=0)
      name = input_file_param_util.get_variable_name(name)
      input_data.add(input_file_param_util.make_param(name, value, recursive))

  # For output files, we need to:
  #   * split the input into name=uri pairs (name optional)
  #   * get the environmental variable name, or automatically set if null.
  #   * create the output file param
  output_data = set()
  for (recursive, args) in ((False, outputs), (True, outputs_recursive)):
    for arg in args:
      name, value = split_pair(arg, '=', 0)
      name = output_file_param_util.get_variable_name(name)
      output_data.add(output_file_param_util.make_param(name, value, recursive))

  mount_data = set()
  for arg in mounts:
    # Mounts can look like `--mount VAR=PATH` or `--mount VAR=PATH {num}`,
    # where num is the size of the disk in Gb. We assume a space is the
    # separator between path and disk size.
    if ' ' in arg:
      key_value_pair, disk_size = arg.split(' ')
      name, value = split_pair(key_value_pair, '=', 1)
      mount_data.add(mount_param_util.make_param(name, value, disk_size))
    else:
      name, value = split_pair(arg, '=', 1)
      mount_data.add(mount_param_util.make_param(name, value, disk_size=None))
  return {
      'envs': env_data,
      'inputs': input_data,
      'outputs': output_data,
      'labels': label_data,
      'mounts': mount_data,
  }