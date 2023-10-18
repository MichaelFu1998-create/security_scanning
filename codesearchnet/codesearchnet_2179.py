def reset(self):
        """
        Resets the model to its initial state on episode start. This should also reset all preprocessor(s).

        Returns:
            tuple:
                Current episode, timestep counter and the shallow-copied list of internal state initialization Tensors.
        """
        fetches = [self.global_episode, self.global_timestep]

        # Loop through all preprocessors and reset them as well.
        for name in sorted(self.states_preprocessing):
            fetch = self.states_preprocessing[name].reset()
            if fetch is not None:
                fetches.extend(fetch)

        if self.flush_summarizer is not None:
            fetches.append(self.flush_summarizer)

        # Get the updated episode and timestep counts.
        fetch_list = self.monitored_session.run(fetches=fetches)
        episode, timestep = fetch_list[:2]

        return episode, timestep, self.internals_init