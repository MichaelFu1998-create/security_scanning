def get_action_by_id(op, action_id):
  """Return the operation's array of actions."""
  actions = get_actions(op)
  if actions and 1 <= action_id < len(actions):
    return actions[action_id - 1]