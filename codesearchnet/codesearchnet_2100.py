def _run_single(self, thread_id, agent, environment, deterministic=False,
                    max_episode_timesteps=-1, episode_finished=None, testing=False, sleep=None):
        """
        The target function for a thread, runs an agent and environment until signaled to stop.
        Adds rewards to shared episode rewards list.

        Args:
            thread_id (int): The ID of the thread that's running this target function.
            agent (Agent): The Agent object that this particular thread uses.
            environment (Environment): The Environment object that this particular thread uses.
            max_episode_timesteps (int): Max. number of timesteps per episode. Use -1 or 0 for non-limited episodes.
            episode_finished (callable): Function called after each episode that takes an episode summary spec and
                returns False, if this single run should terminate after this episode.
                Can be used e.g. to set a particular mean reward threshold.
        """

        # figure out whether we are using the deprecated way of "episode_finished" reporting
        old_episode_finished = False
        if episode_finished is not None and len(getargspec(episode_finished).args) == 1:
            old_episode_finished = True

        episode = 0
        # Run this single worker (episode loop) as long as global count thresholds have not been reached.
        while not self.should_stop:
            state = environment.reset()
            agent.reset()
            self.global_timestep, self.global_episode = agent.timestep, agent.episode
            episode_reward = 0

            # Time step (within episode) loop
            time_step = 0
            time_start = time.time()
            while True:
                action, internals, states = agent.act(states=state, deterministic=deterministic, buffered=False)
                reward = 0
                for repeat in xrange(self.repeat_actions):
                    state, terminal, step_reward = environment.execute(action=action)
                    reward += step_reward
                    if terminal:
                        break

                if not testing:
                    # agent.observe(reward=reward, terminal=terminal)
                    # Insert everything at once.
                    agent.atomic_observe(
                        states=state,
                        actions=action,
                        internals=internals,
                        reward=reward,
                        terminal=terminal
                    )

                if sleep is not None:
                    time.sleep(sleep)

                time_step += 1
                episode_reward += reward

                if terminal or time_step == max_episode_timesteps:
                    break

                # Abort the episode (discard its results) when global says so.
                if self.should_stop:
                    return

            self.global_timestep += time_step

            # Avoid race condition where order in episode_rewards won't match order in episode_timesteps.
            self.episode_list_lock.acquire()
            self.episode_rewards.append(episode_reward)
            self.episode_timesteps.append(time_step)
            self.episode_times.append(time.time() - time_start)
            self.episode_list_lock.release()

            if episode_finished is not None:
                # old way of calling episode_finished
                if old_episode_finished:
                    summary_data = {
                        "thread_id": thread_id,
                        "episode": episode,
                        "timestep": time_step,
                        "episode_reward": episode_reward
                    }
                    if not episode_finished(summary_data):
                        return
                # New way with BasicRunner (self) and thread-id.
                elif not episode_finished(self, thread_id):
                    return

            episode += 1