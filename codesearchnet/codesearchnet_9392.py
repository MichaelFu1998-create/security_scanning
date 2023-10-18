def _prepare_row(task, full, summary):
  """return a dict with the task's info (more if "full" is set)."""

  # Would like to include the Job ID in the default set of columns, but
  # it is a long value and would leave little room for status and update time.

  row_spec = collections.namedtuple('row_spec',
                                    ['key', 'required', 'default_value'])

  # pyformat: disable
  default_columns = [
      row_spec('job-name', True, None),
      row_spec('task-id', False, None),
      row_spec('last-update', True, None),
      row_spec('status-message', True, None)
  ]
  full_columns = default_columns + [
      row_spec('job-id', True, None),
      row_spec('user-id', True, None),
      row_spec('status', True, None),
      row_spec('status-detail', True, None),
      row_spec('task-attempt', False, None),
      row_spec('create-time', True, None),
      row_spec('start-time', True, None),
      row_spec('end-time', True, None),
      row_spec('internal-id', True, None),
      row_spec('logging', True, None),
      row_spec('labels', True, {}),
      row_spec('envs', True, {}),
      row_spec('inputs', True, {}),
      row_spec('input-recursives', False, {}),
      row_spec('outputs', True, {}),
      row_spec('output-recursives', False, {}),
      row_spec('mounts', True, {}),
      row_spec('provider', True, None),
      row_spec('provider-attributes', True, {}),
      row_spec('events', True, []),
      row_spec('user-project', False, None),
      row_spec('dsub-version', False, None),
      row_spec('script-name', False, None),
      row_spec('script', False, None),
  ]
  summary_columns = default_columns + [
      row_spec('job-id', True, None),
      row_spec('user-id', True, None),
      row_spec('status', True, None),
  ]
  # pyformat: enable

  assert not (full and summary), 'Full and summary cannot both be enabled'

  if full:
    columns = full_columns
  elif summary:
    columns = summary_columns
  else:
    columns = default_columns

  row = {}
  for col in columns:
    key, required, default = col

    value = task.get_field(key, default)
    if required or value is not None:
      row[key] = value

  return row