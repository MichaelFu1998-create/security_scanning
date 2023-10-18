def tasks_file_to_task_descriptors(tasks, retries, input_file_param_util,
                                   output_file_param_util):
  """Parses task parameters from a TSV.

  Args:
    tasks: Dict containing the path to a TSV file and task numbers to run
    variables, input, and output parameters as column headings. Subsequent
    lines specify parameter values, one row per job.
    retries: Number of retries allowed.
    input_file_param_util: Utility for producing InputFileParam objects.
    output_file_param_util: Utility for producing OutputFileParam objects.

  Returns:
    task_descriptors: an array of records, each containing the task-id,
    task-attempt, 'envs', 'inputs', 'outputs', 'labels' that defines the set of
    parameters for each task of the job.

  Raises:
    ValueError: If no job records were provided
  """
  task_descriptors = []

  path = tasks['path']
  task_min = tasks.get('min')
  task_max = tasks.get('max')

  # Load the file and set up a Reader that tokenizes the fields
  param_file = dsub_util.load_file(path)
  reader = csv.reader(param_file, delimiter='\t')

  # Read the first line and extract the parameters
  header = six.advance_iterator(reader)
  job_params = parse_tasks_file_header(header, input_file_param_util,
                                       output_file_param_util)

  # Build a list of records from the parsed input file
  for row in reader:
    # Tasks are numbered starting at 1 and since the first line of the TSV
    # file is a header, the first task appears on line 2.
    task_id = reader.line_num - 1
    if task_min and task_id < task_min:
      continue
    if task_max and task_id > task_max:
      continue

    if len(row) != len(job_params):
      dsub_util.print_error('Unexpected number of fields %s vs %s: line %s' %
                            (len(row), len(job_params), reader.line_num))

    # Each row can contain "envs", "inputs", "outputs"
    envs = set()
    inputs = set()
    outputs = set()
    labels = set()

    for i in range(0, len(job_params)):
      param = job_params[i]
      name = param.name
      if isinstance(param, job_model.EnvParam):
        envs.add(job_model.EnvParam(name, row[i]))

      elif isinstance(param, job_model.LabelParam):
        labels.add(job_model.LabelParam(name, row[i]))

      elif isinstance(param, job_model.InputFileParam):
        inputs.add(
            input_file_param_util.make_param(name, row[i], param.recursive))

      elif isinstance(param, job_model.OutputFileParam):
        outputs.add(
            output_file_param_util.make_param(name, row[i], param.recursive))

    task_descriptors.append(
        job_model.TaskDescriptor({
            'task-id': task_id,
            'task-attempt': 1 if retries else None
        }, {
            'labels': labels,
            'envs': envs,
            'inputs': inputs,
            'outputs': outputs
        }, job_model.Resources()))

  # Ensure that there are jobs to execute (and not just a header)
  if not task_descriptors:
    raise ValueError('No tasks added from %s' % path)

  return task_descriptors