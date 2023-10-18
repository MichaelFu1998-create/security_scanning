def run(command, parser, cl_args, unknown_args):
  '''
  :param command:
  :param parser:
  :param args:
  :param unknown_args:
  :return:
  '''
  configcommand = cl_args.get('configcommand', None)
  if configcommand == 'set':
    return _set(cl_args)
  elif configcommand == 'unset':
    return _unset(cl_args)
  else:
    return _list(cl_args)