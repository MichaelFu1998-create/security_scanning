def _run_post(self, run_steps):
    """
    If Naarad is run in CLI mode, execute any post run steps specified in the config
    :param: run_steps: list of post run steps
    """
    for run_step in sorted(run_steps, key=lambda step: step.run_rank):
      run_step.run()
    return CONSTANTS.OK