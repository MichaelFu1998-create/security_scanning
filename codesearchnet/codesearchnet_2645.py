def get_command_handlers():
  '''
  Create a map of command names and handlers
  '''
  return {
      'activate': activate,
      'config': hconfig,
      'deactivate': deactivate,
      'help': cli_help,
      'kill': kill,
      'restart': restart,
      'submit': submit,
      'update': update,
      'version': version
  }