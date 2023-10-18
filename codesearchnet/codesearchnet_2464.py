def run(command, parser, cl_args, unknown_args):
  '''
  :param command:
  :param parser:
  :param cl_args:
  :param unknown_args:
  :return:
  '''
  Log.debug("Deactivate Args: %s", cl_args)
  return cli_helper.run(command, cl_args, "deactivate topology")