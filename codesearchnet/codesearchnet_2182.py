def observe(self, terminal, reward, index=0):
        """
        Adds an observation (reward and is-terminal) to the model without updating its trainable variables.

        Args:
            terminal (List[bool]): List of is-terminal signals.
            reward (List[float]): List of reward signals.
            index: (int) parallel episode you want to observe

        Returns:
            The value of the model-internal episode counter.
        """
        fetches = self.episode_output
        feed_dict = self.get_feed_dict(terminal=terminal, reward=reward, index=index)

        episode = self.monitored_session.run(fetches=fetches, feed_dict=feed_dict)

        return episode