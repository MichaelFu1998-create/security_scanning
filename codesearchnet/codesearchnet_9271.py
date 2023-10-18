def get_filter(project,
                 status=None,
                 user_id=None,
                 job_id=None,
                 job_name=None,
                 labels=None,
                 task_id=None,
                 task_attempt=None,
                 create_time_min=None,
                 create_time_max=None):
    """Return a filter string for operations.list()."""

    ops_filter = ['projectId = %s' % project]
    if status and status != '*':
      ops_filter.append('status = %s' % status)

    if user_id != '*':
      ops_filter.append('labels.user-id = %s' % user_id)
    if job_id != '*':
      ops_filter.append('labels.job-id = %s' % job_id)
    if job_name != '*':
      ops_filter.append('labels.job-name = %s' % job_name)
    if task_id != '*':
      ops_filter.append('labels.task-id = %s' % task_id)
    if task_attempt != '*':
      ops_filter.append('labels.task-attempt = %s' % task_attempt)

    # Even though labels are nominally 'arbitrary strings' they are trusted
    # since param_util restricts the character set.
    if labels:
      for l in labels:
        ops_filter.append('labels.%s = %s' % (l.name, l.value))

    epoch = dsub_util.replace_timezone(datetime.utcfromtimestamp(0), pytz.utc)
    if create_time_min:
      create_time_min_utc_int = (create_time_min - epoch).total_seconds()
      ops_filter.append('createTime >= %d' % create_time_min_utc_int)
    if create_time_max:
      create_time_max_utc_int = (create_time_max - epoch).total_seconds()
      ops_filter.append('createTime <= %d' % create_time_max_utc_int)

    return ' AND '.join(ops_filter)