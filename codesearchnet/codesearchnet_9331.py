def _group_tasks_by_jobid(tasks):
  """A defaultdict with, for each job, a list of its tasks."""
  ret = collections.defaultdict(list)
  for t in tasks:
    ret[t.get_field('job-id')].append(t)
  return ret