def run(handlers, command, parser, command_args, unknown_args):
  '''
  Run the command
  :param command:
  :param parser:
  :param command_args:
  :param unknown_args:
  :return:
  '''

  if command in handlers:
    return handlers[command].run(command, parser, command_args, unknown_args)
  else:
    err_context = 'Unknown subcommand: %s' % command
    return result.SimpleResult(result.Status.InvocationError, err_context)