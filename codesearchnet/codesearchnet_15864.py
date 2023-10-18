def _run_pre(self, analysis, run_steps):
    """
    If Naarad is run in CLI mode, execute any pre run steps specified in the config. ts_start/ts_end are set based on
    workload run steps if any.
    :param: analysis: The analysis object being processed
    :param: run_steps: list of post run steps
    """
    workload_run_steps = []
    for run_step in sorted(run_steps, key=lambda step: step.run_rank):
      run_step.run()
      if run_step.run_type == CONSTANTS.RUN_TYPE_WORKLOAD:
        workload_run_steps.append(run_step)
    # Get analysis time period from workload run steps
    if len(workload_run_steps) > 0:
      analysis.ts_start, analysis.ts_end = naarad.utils.get_run_time_period(workload_run_steps)
    return CONSTANTS.OK