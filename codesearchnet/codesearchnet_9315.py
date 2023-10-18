def lookup_job_tasks(self,
                       statuses,
                       user_ids=None,
                       job_ids=None,
                       job_names=None,
                       task_ids=None,
                       task_attempts=None,
                       labels=None,
                       create_time_min=None,
                       create_time_max=None,
                       max_tasks=0):
    """Return a list of operations. See base.py for additional detail."""
    statuses = None if statuses == {'*'} else statuses
    user_ids = None if user_ids == {'*'} else user_ids
    job_ids = None if job_ids == {'*'} else job_ids
    job_names = None if job_names == {'*'} else job_names
    task_ids = None if task_ids == {'*'} else task_ids
    task_attempts = None if task_attempts == {'*'} else task_attempts

    if labels or create_time_min or create_time_max:
      raise NotImplementedError(
          'Lookup by labels and create_time not yet supported by stub.')

    operations = [
        x for x in self._operations
        if ((not statuses or x.get_field('status', (None, None))[0] in statuses
            ) and (not user_ids or x.get_field('user', None) in user_ids) and
            (not job_ids or x.get_field('job-id', None) in job_ids) and
            (not job_names or x.get_field('job-name', None) in job_names) and
            (not task_ids or x.get_field('task-id', None) in task_ids) and
            (not task_attempts or
             x.get_field('task-attempt', None) in task_attempts))
    ]
    if max_tasks > 0:
      operations = operations[:max_tasks]
    return operations