def tf_discounted_cumulative_reward(self, terminal, reward, discount=None, final_reward=0.0, horizon=0):
        """
        Creates and returns the TensorFlow operations for calculating the sequence of discounted cumulative rewards
        for a given sequence of single rewards.

        Example:
        single rewards = 2.0 1.0 0.0 0.5 1.0 -1.0
        terminal = False, False, False, False True False
        gamma = 0.95
        final_reward = 100.0 (only matters for last episode (r=-1.0) as this episode has no terminal signal)
        horizon=3
        output = 2.95 1.45 1.38 1.45 1.0 94.0

        Args:
            terminal: Tensor (bool) holding the is-terminal sequence. This sequence may contain more than one
                True value. If its very last element is False (not terminating), the given `final_reward` value
                is assumed to follow the last value in the single rewards sequence (see below).
            reward: Tensor (float) holding the sequence of single rewards. If the last element of `terminal` is False,
                an assumed last reward of the value of `final_reward` will be used.
            discount (float): The discount factor (gamma). By default, take the Model's discount factor.
            final_reward (float): Reward value to use if last episode in sequence does not terminate (terminal sequence
                ends with False). This value will be ignored if horizon == 1 or discount == 0.0.
            horizon (int): The length of the horizon (e.g. for n-step cumulative rewards in continuous tasks
                without terminal signals). Use 0 (default) for an infinite horizon. Note that horizon=1 leads to the
                exact same results as a discount factor of 0.0.

        Returns:
            Discounted cumulative reward tensor with the same shape as `reward`.
        """

        # By default -> take Model's gamma value
        if discount is None:
            discount = self.discount

        # Accumulates discounted (n-step) reward (start new if terminal)
        def cumulate(cumulative, reward_terminal_horizon_subtract):
            rew, is_terminal, is_over_horizon, sub = reward_terminal_horizon_subtract
            return tf.where(
                # If terminal, start new cumulation.
                condition=is_terminal,
                x=rew,
                y=tf.where(
                    # If we are above the horizon length (H) -> subtract discounted value from H steps back.
                    condition=is_over_horizon,
                    x=(rew + cumulative * discount - sub),
                    y=(rew + cumulative * discount)
                )
            )

        # Accumulates length of episodes (starts new if terminal)
        def len_(cumulative, term):
            return tf.where(
                condition=term,
                # Start counting from 1 after is-terminal signal
                x=tf.ones(shape=(), dtype=tf.int32),
                # Otherwise, increase length by 1
                y=cumulative + 1
            )

        # Reverse, since reward cumulation is calculated right-to-left, but tf.scan only works left-to-right.
        reward = tf.reverse(tensor=reward, axis=(0,))
        # e.g. -1.0 1.0 0.5 0.0 1.0 2.0
        terminal = tf.reverse(tensor=terminal, axis=(0,))
        # e.g. F T F F F F

        # Store the steps until end of the episode(s) determined by the input terminal signals (True starts new count).
        lengths = tf.scan(fn=len_, elems=terminal, initializer=0)
        # e.g. 1 1 2 3 4 5
        off_horizon = tf.greater(lengths, tf.fill(dims=tf.shape(lengths), value=horizon))
        # e.g. F F F F T T

        # Calculate the horizon-subtraction value for each step.
        if horizon > 0:
            horizon_subtractions = tf.map_fn(lambda x: (discount ** horizon) * x, reward, dtype=tf.float32)
            # Shift right by size of horizon (fill rest with 0.0).
            horizon_subtractions = tf.concat([np.zeros(shape=(horizon,)), horizon_subtractions], axis=0)
            horizon_subtractions = tf.slice(horizon_subtractions, begin=(0,), size=tf.shape(reward))
            # e.g. 0.0, 0.0, 0.0, -1.0*g^3, 1.0*g^3, 0.5*g^3
        # all 0.0 if infinite horizon (special case: horizon=0)
        else:
            horizon_subtractions = tf.zeros(shape=tf.shape(reward))

        # Now do the scan, each time summing up the previous step (discounted by gamma) and
        # subtracting the respective `horizon_subtraction`.
        reward = tf.scan(
            fn=cumulate,
            elems=(reward, terminal, off_horizon, horizon_subtractions),
            initializer=final_reward if horizon != 1 else 0.0
        )
        # Re-reverse again to match input sequences.
        return tf.reverse(tensor=reward, axis=(0,))