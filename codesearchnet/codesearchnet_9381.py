def _emit_search_criteria(user_ids, job_ids, task_ids, labels):
  """Print the filters used to delete tasks. Use raw flags as arguments."""
  print('Delete running jobs:')
  print('  user:')
  print('    %s\n' % user_ids)
  print('  job-id:')
  print('    %s\n' % job_ids)
  if task_ids:
    print('  task-id:')
    print('    %s\n' % task_ids)
  # Labels are in a LabelParam namedtuple and must be reformated for printing.
  if labels:
    print('  labels:')
    print('    %s\n' % repr(labels))