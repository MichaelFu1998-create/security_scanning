def get_action_environment(op, name):
  """Return the environment for the operation."""
  action = _get_action_by_name(op, name)
  if action:
    return action.get('environment')