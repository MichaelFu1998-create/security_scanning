def tf_preprocess(self, states, actions, reward):
        """
        Applies preprocessing ops to the raw states/action/reward inputs.

        Args:
            states (dict): Dict of raw state tensors.
            actions (dict): Dict or raw action tensors.
            reward: 1D (float) raw rewards tensor.

        Returns: The preprocessed versions of the input tensors.
        """
        # States preprocessing
        for name in sorted(self.states_preprocessing):
            states[name] = self.states_preprocessing[name].process(tensor=states[name])

        # Reward preprocessing
        if self.reward_preprocessing is not None:
            reward = self.reward_preprocessing.process(tensor=reward)

        return states, actions, reward