def choice_action_by_probs(probs=(0.5, 0.5), action_list=None):
    """Choice and return an an action by given the action probability distribution.

    Parameters
    ------------
    probs : list of float.
        The probability distribution of all actions.
    action_list : None or a list of int or others
        A list of action in integer, string or others. If None, returns an integer range between 0 and len(probs)-1.

    Returns
    --------
    float int or str
        The chosen action.

    Examples
    ----------
    >>> for _ in range(5):
    >>>     a = choice_action_by_probs([0.2, 0.4, 0.4])
    >>>     print(a)
    0
    1
    1
    2
    1
    >>> for _ in range(3):
    >>>     a = choice_action_by_probs([0.5, 0.5], ['a', 'b'])
    >>>     print(a)
    a
    b
    b

    """
    if action_list is None:
        n_action = len(probs)
        action_list = np.arange(n_action)
    else:
        if len(action_list) != len(probs):
            raise Exception("number of actions should equal to number of probabilities.")
    return np.random.choice(action_list, p=probs)