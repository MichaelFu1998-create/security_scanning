def _prepare_summary_table(rows):
  """Create a new table that is a summary of the input rows.

  All with the same (job-name or job-id, status) go together.

  Args:
    rows: the input rows, a list of dictionaries.
  Returns:
    A new row set of summary information.
  """
  if not rows:
    return []

  # We either group on the job-name (if present) or fall back to the job-id
  key_field = 'job-name'
  if key_field not in rows[0]:
    key_field = 'job-id'

  # Group each of the rows based on (job-name or job-id, status)
  grouped = collections.defaultdict(lambda: collections.defaultdict(lambda: []))
  for row in rows:
    grouped[row.get(key_field, '')][row.get('status', '')] += [row]

  # Now that we have the rows grouped, create a summary table.
  # Use the original table as the driver in order to preserve the order.
  new_rows = []
  for job_key in sorted(grouped.keys()):
    group = grouped.get(job_key, None)
    canonical_status = ['RUNNING', 'SUCCESS', 'FAILURE', 'CANCEL']
    # Written this way to ensure that if somehow a new status is introduced,
    # it shows up in our output.
    for status in canonical_status + sorted(group.keys()):
      if status not in group:
        continue
      task_count = len(group[status])
      del group[status]
      if task_count:
        summary_row = collections.OrderedDict()
        summary_row[key_field] = job_key
        summary_row['status'] = status
        summary_row['task-count'] = task_count
        new_rows.append(summary_row)

  return new_rows