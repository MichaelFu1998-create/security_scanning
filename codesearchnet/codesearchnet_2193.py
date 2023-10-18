def sanity_check_states(states_spec):
    """
    Sanity checks a states dict, used to define the state space for an MDP.
    Throws an error or warns if mismatches are found.

    Args:
        states_spec (Union[None,dict]): The spec-dict to check (or None).

    Returns: Tuple of 1) the state space desc and 2) whether there is only one component in the state space.
    """
    # Leave incoming states dict intact.
    states = copy.deepcopy(states_spec)

    # Unique state shortform.
    is_unique = ('shape' in states)
    if is_unique:
        states = dict(state=states)

    # Normalize states.
    for name, state in states.items():
        # Convert int to unary tuple.
        if isinstance(state['shape'], int):
            state['shape'] = (state['shape'],)

        # Set default type to float.
        if 'type' not in state:
            state['type'] = 'float'

    return states, is_unique