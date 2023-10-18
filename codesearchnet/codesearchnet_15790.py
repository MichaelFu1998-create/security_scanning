def get_variables(args):
  """
  Return a dictionary of variables specified at CLI
  :param: args: Command Line Arguments namespace
  """
  variables_dict = {}
  if args.variables:
    for var in args.variables:
      words = var.split('=')
      variables_dict[words[0]] = words[1]
  return variables_dict