def _get_action_by_name(op, name):
  """Return the value for the specified action."""
  actions = get_actions(op)
  for action in actions:
    if action.get('name') == name:
      return action