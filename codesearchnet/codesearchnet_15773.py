def get_run_time_period(run_steps):
  """
  This method finds the time range which covers all the Run_Steps

  :param run_steps: list of Run_Step objects
  :return: tuple of start and end timestamps
  """
  init_ts_start = get_standardized_timestamp('now', None)
  ts_start = init_ts_start
  ts_end = '0'
  for run_step in run_steps:
    if run_step.ts_start and run_step.ts_end:
      if run_step.ts_start < ts_start:
        ts_start = run_step.ts_start
      if run_step.ts_end > ts_end:
        ts_end = run_step.ts_end
  if ts_end == '0':
    ts_end = None
  if ts_start == init_ts_start:
    ts_start = None
  logger.info('get_run_time_period range returned ' + str(ts_start) + ' to ' + str(ts_end))
  return ts_start, ts_end