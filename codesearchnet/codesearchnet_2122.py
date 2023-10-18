def tf_reference(self, states, internals, actions, terminal, reward, next_states, next_internals, update):
        """
        Creates the TensorFlow operations for obtaining the reference tensor(s), in case of a
        comparative loss.

        Args:
            states: Dict of state tensors.
            internals: List of prior internal state tensors.
            actions: Dict of action tensors.
            terminal: Terminal boolean tensor.
            reward: Reward tensor.
            next_states: Dict of successor state tensors.
            next_internals: List of posterior internal state tensors.
            update: Boolean tensor indicating whether this call happens during an update.

        Returns:
            Reference tensor(s).
        """
        return None