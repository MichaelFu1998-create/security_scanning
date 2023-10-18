def parse_run_step_section(config_obj, section):
  """
  Parse a RUN-STEP section in the config to return a Run_Step object
  :param config_obj: ConfigParser objection
  :param section: Section name
  :return: an initialized Run_Step object
  """
  kill_after_seconds = None
  try:
    run_cmd = config_obj.get(section, 'run_cmd')
    run_rank = int(config_obj.get(section, 'run_rank'))
  except ConfigParser.NoOptionError:
    logger.exception("Exiting.... some mandatory options are missing from the config file in section: " + section)
    sys.exit()
  except ValueError:
    logger.error("Bad run_rank %s specified in section %s, should be integer. Exiting.", config_obj.get(section, 'run_rank'), section)
    sys.exit()
  if config_obj.has_option(section, 'run_type'):
    run_type = config_obj.get(section, 'run_type')
  else:
    run_type = CONSTANTS.RUN_TYPE_WORKLOAD
  if config_obj.has_option(section, 'run_order'):
    run_order = config_obj.get(section, 'run_order')
  else:
    run_order = CONSTANTS.PRE_ANALYSIS_RUN
  if config_obj.has_option(section, 'call_type'):
    call_type = config_obj.get(section, 'call_type')
  else:
    call_type = 'local'
  if config_obj.has_option(section, 'kill_after_seconds'):
    try:
      kill_after_seconds = int(config_obj.get(section, 'kill_after_seconds'))
    except ValueError:
      logger.error("Bad kill_after_seconds %s specified in section %s, should be integer.", config_obj.get(section, 'kill_after_seconds'), section)

  if call_type == 'local':
    run_step_obj = Local_Cmd(run_type, run_cmd, call_type, run_order, run_rank, kill_after_seconds=kill_after_seconds)
  else:
    logger.error('Unsupported RUN_STEP supplied, call_type should be local')
    run_step_obj = None
  return run_step_obj