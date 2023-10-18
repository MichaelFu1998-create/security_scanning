def create_operations(self, states, internals, actions, terminal, reward, deterministic, independent, index):
        """
        Creates and stores tf operations for when `act()` and `observe()` are called.
        """
        self.create_act_operations(
            states=states,
            internals=internals,
            deterministic=deterministic,
            independent=independent,
            index=index
        )
        self.create_observe_operations(
            reward=reward,
            terminal=terminal,
            index=index
        )
        self.create_atomic_observe_operations(
            states=states,
            actions=actions,
            internals=internals,
            reward=reward,
            terminal=terminal,
            index=index
        )