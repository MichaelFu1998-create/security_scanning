def get_action_image(op, name):
  """Return the image for the operation."""
  action = _get_action_by_name(op, name)
  if action:
    return action.get('imageUri')