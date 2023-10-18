def discount_episode_rewards(rewards=None, gamma=0.99, mode=0):
    """Take 1D float array of rewards and compute discounted rewards for an
    episode. When encount a non-zero value, consider as the end a of an episode.

    Parameters
    ----------
    rewards : list
        List of rewards
    gamma : float
        Discounted factor
    mode : int
        Mode for computing the discount rewards.
            - If mode == 0, reset the discount process when encount a non-zero reward (Ping-pong game).
            - If mode == 1, would not reset the discount process.

    Returns
    --------
    list of float
        The discounted rewards.

    Examples
    ----------
    >>> rewards = np.asarray([0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1])
    >>> gamma = 0.9
    >>> discount_rewards = tl.rein.discount_episode_rewards(rewards, gamma)
    >>> print(discount_rewards)
    [ 0.72899997  0.81        0.89999998  1.          0.72899997  0.81
    0.89999998  1.          0.72899997  0.81        0.89999998  1.        ]
    >>> discount_rewards = tl.rein.discount_episode_rewards(rewards, gamma, mode=1)
    >>> print(discount_rewards)
    [ 1.52110755  1.69011939  1.87791049  2.08656716  1.20729685  1.34144104
    1.49048996  1.65610003  0.72899997  0.81        0.89999998  1.        ]

    """
    if rewards is None:
        raise Exception("rewards should be a list")
    discounted_r = np.zeros_like(rewards, dtype=np.float32)
    running_add = 0
    for t in reversed(xrange(0, rewards.size)):
        if mode == 0:
            if rewards[t] != 0: running_add = 0

        running_add = running_add * gamma + rewards[t]
        discounted_r[t] = running_add
    return discounted_r