def _get_group_randomstate(rs, seed, group):
        """Return a RandomState, equal to the input unless rs is None.

        When rs is None, try to get the random state from the
        'last_random_state' attribute in `group`. When not available,
        use `seed` to generate a random state. When seed is None the returned
        random state will have a random seed.
        """
        if rs is None:
            rs = np.random.RandomState(seed=seed)
            # Try to set the random state from the last session to preserve
            # a single random stream when simulating timestamps multiple times
            if 'last_random_state' in group._v_attrs:
                rs.set_state(group._v_attrs['last_random_state'])
                print("INFO: Random state set to last saved state in '%s'." %
                      group._v_name)
            else:
                print("INFO: Random state initialized from seed (%d)." % seed)
        return rs