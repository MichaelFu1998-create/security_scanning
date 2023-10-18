def run_main(args):
  """Execute job/task submission from command-line arguments."""

  if args.command and args.script:
    raise ValueError('Cannot supply both a --command and --script flag')

  provider_base.check_for_unsupported_flag(args)

  # Set up job parameters and job data from a tasks file or flags.
  input_file_param_util = param_util.InputFileParamUtil(
      DEFAULT_INPUT_LOCAL_PATH)
  output_file_param_util = param_util.OutputFileParamUtil(
      DEFAULT_OUTPUT_LOCAL_PATH)
  mount_param_util = param_util.MountParamUtil(DEFAULT_MOUNT_LOCAL_PATH)

  # Get job arguments from the command line
  job_params = param_util.args_to_job_params(
      args.env, args.label, args.input, args.input_recursive, args.output,
      args.output_recursive, args.mount, input_file_param_util,
      output_file_param_util, mount_param_util)
  # If --tasks is on the command-line, then get task-specific data
  if args.tasks:
    task_descriptors = param_util.tasks_file_to_task_descriptors(
        args.tasks, args.retries, input_file_param_util, output_file_param_util)

    # Validate job data + task data
    _validate_job_and_task_arguments(job_params, task_descriptors)
  else:
    # Create the implicit task
    task_metadata = {'task-id': None}
    if args.retries:
      task_metadata['task-attempt'] = 1
    task_descriptors = [
        job_model.TaskDescriptor(task_metadata, {
            'labels': set(),
            'envs': set(),
            'inputs': set(),
            'outputs': set()
        }, job_model.Resources())
    ]

  return run(
      provider_base.get_provider(args, resources),
      _get_job_resources(args),
      job_params,
      task_descriptors,
      name=args.name,
      dry_run=args.dry_run,
      command=args.command,
      script=args.script,
      user=args.user,
      user_project=args.user_project,
      wait=args.wait,
      retries=args.retries,
      poll_interval=args.poll_interval,
      after=args.after,
      skip=args.skip,
      project=args.project,
      disable_warning=True,
      unique_job_id=args.unique_job_id)