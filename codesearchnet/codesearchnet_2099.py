def run(
        self,
        num_episodes=-1,
        max_episode_timesteps=-1,
        episode_finished=None,
        summary_report=None,
        summary_interval=0,
        num_timesteps=None,
        deterministic=False,
        episodes=None,
        max_timesteps=None,
        testing=False,
        sleep=None
    ):
        """
        Executes this runner by starting all Agents in parallel (each one in one thread).

        Args:
            episodes (int): Deprecated; see num_episodes.
            max_timesteps (int): Deprecated; see max_episode_timesteps.
        """

        # Renamed episodes into num_episodes to match BaseRunner's signature (fully backw. compatible).
        if episodes is not None:
            num_episodes = episodes
            warnings.warn("WARNING: `episodes` parameter is deprecated, use `num_episodes` instead.",
                          category=DeprecationWarning)
        assert isinstance(num_episodes, int)
        # Renamed max_timesteps into max_episode_timesteps to match single Runner's signature (fully backw. compatible).
        if max_timesteps is not None:
            max_episode_timesteps = max_timesteps
            warnings.warn("WARNING: `max_timesteps` parameter is deprecated, use `max_episode_timesteps` instead.",
                          category=DeprecationWarning)
        assert isinstance(max_episode_timesteps, int)

        if summary_report is not None:
            warnings.warn("WARNING: `summary_report` parameter is deprecated, use `episode_finished` callback "
                          "instead to generate summaries every n episodes.",
                          category=DeprecationWarning)

        self.reset()

        # Reset counts/stop-condition for this run.
        self.global_episode = 0
        self.global_timestep = 0
        self.should_stop = False

        # Create threads.
        threads = [threading.Thread(target=self._run_single, args=(t, self.agent[t], self.environment[t],),
                                    kwargs={"deterministic": deterministic,
                                            "max_episode_timesteps": max_episode_timesteps,
                                            "episode_finished": episode_finished,
                                            "testing": testing,
                                            "sleep": sleep})
                   for t in range(len(self.agent))]

        # Start threads.
        self.start_time = time.time()
        [t.start() for t in threads]

        # Stay idle until killed by SIGINT or a global stop condition is met.
        try:
            next_summary = 0
            next_save = 0 if self.save_frequency_unit != "s" else time.time()
            while any([t.is_alive() for t in threads]) and self.global_episode < num_episodes or num_episodes == -1:
                self.time = time.time()

                # This is deprecated (but still supported) and should be covered by the `episode_finished` callable.
                if summary_report is not None and self.global_episode > next_summary:
                    summary_report(self)
                    next_summary += summary_interval

                if self.save_path and self.save_frequency is not None:
                    do_save = True
                    current = None
                    if self.save_frequency_unit == "e" and self.global_episode > next_save:
                        current = self.global_episode
                    elif self.save_frequency_unit == "s" and self.time > next_save:
                        current = self.time
                    elif self.save_frequency_unit == "t" and self.global_timestep > next_save:
                        current = self.global_timestep
                    else:
                        do_save = False

                    if do_save:
                        self.agent[0].save_model(self.save_path)
                        # Make sure next save is later than right now.
                        while next_save < current:
                            next_save += self.save_frequency
                time.sleep(1)

        except KeyboardInterrupt:
            print('Keyboard interrupt, sending stop command to threads')

        self.should_stop = True

        # Join threads.
        [t.join() for t in threads]
        print('All threads stopped')