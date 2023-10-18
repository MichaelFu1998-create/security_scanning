def insert_bool(param, command_args):
  '''
  :param param:
  :param command_args:
  :return:
  '''
  index = 0
  found = False
  for lelem in command_args:
    if lelem == '--' and not found:
      break
    if lelem == param:
      found = True
      break
    index = index + 1

  if found:
    command_args.insert(index + 1, 'True')
  return command_args