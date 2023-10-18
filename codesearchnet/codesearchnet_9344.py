def parse_pair_args(labels, argclass):
  """Parse flags of key=value pairs and return a list of argclass.

  For pair variables, we need to:
     * split the input into name=value pairs (value optional)
     * Create the EnvParam object

  Args:
    labels: list of 'key' or 'key=value' strings.
    argclass: Container class for args, must instantiate with argclass(k, v).

  Returns:
    list of argclass objects.
  """
  label_data = set()
  for arg in labels:
    name, value = split_pair(arg, '=', nullable_idx=1)
    label_data.add(argclass(name, value))
  return label_data