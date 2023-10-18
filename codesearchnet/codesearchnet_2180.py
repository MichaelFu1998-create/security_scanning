def get_feed_dict(
        self,
        states=None,
        internals=None,
        actions=None,
        terminal=None,
        reward=None,
        deterministic=None,
        independent=None,
        index=None
    ):
        """
        Returns the feed-dict for the model's acting and observing tf fetches.

        Args:
            states (dict): Dict of state values (each key represents one state space component).
            internals (dict): Dict of internal state values (each key represents one internal state component).
            actions (dict): Dict of actions (each key represents one action space component).
            terminal (List[bool]): List of is-terminal signals.
            reward (List[float]): List of reward signals.
            deterministic (bool): Whether actions should be picked without exploration.
            independent (bool): Whether we are doing an independent act (not followed by call to observe;
                not to be stored in model's buffer).

        Returns: The feed dict to use for the fetch.
        """
        feed_dict = dict()
        batched = None

        if states is not None:
            if batched is None:
                name = next(iter(states))
                state = np.asarray(states[name])
                batched = (state.ndim != len(self.states_spec[name]['unprocessed_shape']))
            if batched:
                feed_dict.update({self.states_input[name]: states[name] for name in sorted(self.states_input)})
            else:
                feed_dict.update({self.states_input[name]: (states[name],) for name in sorted(self.states_input)})

        if internals is not None:
            if batched is None:
                name = next(iter(internals))
                internal = np.asarray(internals[name])
                batched = (internal.ndim != len(self.internals_spec[name]['shape']))
            if batched:
                feed_dict.update({self.internals_input[name]: internals[name] for name in sorted(self.internals_input)})
            else:
                feed_dict.update({self.internals_input[name]: (internals[name],) for name in sorted(self.internals_input)})

        if actions is not None:
            if batched is None:
                name = next(iter(actions))
                action = np.asarray(actions[name])
                batched = (action.ndim != len(self.actions_spec[name]['shape']))
            if batched:
                feed_dict.update({self.actions_input[name]: actions[name] for name in sorted(self.actions_input)})
            else:
                feed_dict.update({self.actions_input[name]: (actions[name],) for name in sorted(self.actions_input)})

        if terminal is not None:
            if batched is None:
                terminal = np.asarray(terminal)
                batched = (terminal.ndim == 1)
            if batched:
                feed_dict[self.terminal_input] = terminal
            else:
                feed_dict[self.terminal_input] = (terminal,)

        if reward is not None:
            if batched is None:
                reward = np.asarray(reward)
                batched = (reward.ndim == 1)
            if batched:
                feed_dict[self.reward_input] = reward
            else:
                feed_dict[self.reward_input] = (reward,)

        if deterministic is not None:
            feed_dict[self.deterministic_input] = deterministic

        if independent is not None:
            feed_dict[self.independent_input] = independent

        feed_dict[self.episode_index_input] = index

        return feed_dict