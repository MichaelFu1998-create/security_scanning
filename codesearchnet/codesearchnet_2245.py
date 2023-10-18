def tf_import_demo_experience(self, states, internals, actions, terminal, reward):
        """
        Imports a single experience to memory.
        """
        return self.demo_memory.store(
            states=states,
            internals=internals,
            actions=actions,
            terminal=terminal,
            reward=reward
        )