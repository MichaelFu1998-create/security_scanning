def sanity_check_actions(actions_spec):
    """
    Sanity checks an actions dict, used to define the action space for an MDP.
    Throws an error or warns if mismatches are found.

    Args:
        actions_spec (Union[None,dict]): The spec-dict to check (or None).

    Returns: Tuple of 1) the action space desc and 2) whether there is only one component in the action space.
    """
    # Leave incoming spec-dict intact.
    actions = copy.deepcopy(actions_spec)

    # Unique action shortform.
    is_unique = ('type' in actions)
    if is_unique:
        actions = dict(action=actions)

    # Normalize actions.
    for name, action in actions.items():
        # Set default type to int
        if 'type' not in action:
            action['type'] = 'int'

        # Check required values
        if action['type'] == 'int':
            if 'num_actions' not in action:
                raise TensorForceError("Action requires value 'num_actions' set!")
        elif action['type'] == 'float':
            if ('min_value' in action) != ('max_value' in action):
                raise TensorForceError("Action requires both values 'min_value' and 'max_value' set!")

        # Set default shape to empty tuple (single-int, discrete action space)
        if 'shape' not in action:
            action['shape'] = ()

        # Convert int to unary tuple
        if isinstance(action['shape'], int):
            action['shape'] = (action['shape'],)

    return actions, is_unique