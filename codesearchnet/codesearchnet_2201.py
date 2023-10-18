def reset(self, history=None):
        """
        Resets the Runner's internal stats counters.
        If history is empty, use default values in history.get().

        Args:
            history (dict): A dictionary containing an already run experiment's results. Keys should be:
                episode_rewards (list of rewards), episode_timesteps (lengths of episodes), episode_times (run-times)
        """
        if not history:
            history = dict()

        self.episode_rewards = history.get("episode_rewards", list())
        self.episode_timesteps = history.get("episode_timesteps", list())
        self.episode_times = history.get("episode_times", list())