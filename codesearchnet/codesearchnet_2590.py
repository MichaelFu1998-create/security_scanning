def convert_args_dict_to_list(dict_extra_args):
  """ flatten extra args """
  list_extra_args = []
  if 'component_parallelism' in dict_extra_args:
    list_extra_args += ["--component_parallelism",
                        ','.join(dict_extra_args['component_parallelism'])]
  if 'runtime_config' in dict_extra_args:
    list_extra_args += ["--runtime_config",
                        ','.join(dict_extra_args['runtime_config'])]
  if 'container_number' in dict_extra_args:
    list_extra_args += ["--container_number",
                        ','.join(dict_extra_args['container_number'])]
  if 'dry_run' in dict_extra_args and dict_extra_args['dry_run']:
    list_extra_args += ['--dry_run']
  if 'dry_run_format' in dict_extra_args:
    list_extra_args += ['--dry_run_format', dict_extra_args['dry_run_format']]

  return list_extra_args