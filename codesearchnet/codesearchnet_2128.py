def tf_import_experience(self, states, internals, actions, terminal, reward):
        """
        Imports experiences into the TensorFlow memory structure. Can be used to import
        off-policy data.

        :param states: Dict of state values to import with keys as state names and values as values to set.
        :param internals: Internal values to set, can be fetched from agent via agent.current_internals
            if no values available.
        :param actions: Dict of action values to import with keys as action names and values as values to set.
        :param terminal: Terminal value(s)
        :param reward: Reward value(s)
        """
        return self.memory.store(
            states=states,
            internals=internals,
            actions=actions,
            terminal=terminal,
            reward=reward
        )