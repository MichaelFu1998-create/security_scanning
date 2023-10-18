def run(self, num_episodes, num_timesteps, max_episode_timesteps, deterministic, episode_finished, summary_report,
            summary_interval):
        """
        Executes this runner by starting to act (via Agent(s)) in the given Environment(s).
        Stops execution according to certain conditions (e.g. max. number of episodes, etc..).
        Calls callback functions after each episode and/or after some summary criteria are met.

        Args:
            num_episodes (int): Max. number of episodes to run globally in total (across all threads/workers).
            num_timesteps (int): Max. number of time steps to run globally in total (across all threads/workers)
            max_episode_timesteps (int): Max. number of timesteps per episode.
            deterministic (bool): Whether to use exploration when selecting actions.
            episode_finished (callable): A function to be called once an episodes has finished. Should take
                a BaseRunner object and some worker ID (e.g. thread-ID or task-ID). Can decide for itself
                every how many episodes it should report something and what to report.
            summary_report (callable): Deprecated; Function that could produce a summary over the training
                progress so far.
            summary_interval (int): Deprecated; The number of time steps to execute (globally)
                before summary_report is called.
        """
        raise NotImplementedError