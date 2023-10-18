def import_demo_experience(self, states, internals, actions, terminal, reward):
        """
        Stores demonstrations in the demo memory.
        """
        fetches = self.import_demo_experience_output

        feed_dict = self.get_feed_dict(
            states=states,
            internals=internals,
            actions=actions,
            terminal=terminal,
            reward=reward
        )

        self.monitored_session.run(fetches=fetches, feed_dict=feed_dict)