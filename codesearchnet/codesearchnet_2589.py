def build_extra_args_dict(cl_args):
  """ Build extra args map """
  # Check parameters
  component_parallelism = cl_args['component_parallelism']
  runtime_configs = cl_args['runtime_config']
  container_number = cl_args['container_number']
  # Users need to provide either (component-parallelism || container_number) or runtime-config
  if (component_parallelism and runtime_configs) or (container_number and runtime_configs):
    raise Exception(
        "(component-parallelism or container_num) and runtime-config " +
        "can't be updated at the same time")

  dict_extra_args = {}

  nothing_set = True
  if component_parallelism:
    dict_extra_args.update({'component_parallelism': component_parallelism})
    nothing_set = False

  if container_number:
    dict_extra_args.update({'container_number': container_number})
    nothing_set = False

  if runtime_configs:
    dict_extra_args.update({'runtime_config': runtime_configs})
    nothing_set = False

  if nothing_set:
    raise Exception(
        "Missing arguments --component-parallelism or --runtime-config or --container-number")

  if cl_args['dry_run']:
    dict_extra_args.update({'dry_run': True})
    if 'dry_run_format' in cl_args:
      dict_extra_args.update({'dry_run_format': cl_args["dry_run_format"]})

  return dict_extra_args