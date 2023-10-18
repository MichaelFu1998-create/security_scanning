def tf_loss_per_instance(self, states, internals, actions, terminal, reward,
                             next_states, next_internals, update, reference=None):
        """
        Creates the TensorFlow operations for calculating the loss per batch instance.

        Args:
            states: Dict of state tensors.
            internals: Dict of prior internal state tensors.
            actions: Dict of action tensors.
            terminal: Terminal boolean tensor.
            reward: Reward tensor.
            next_states: Dict of successor state tensors.
            next_internals: List of posterior internal state tensors.
            update: Boolean tensor indicating whether this call happens during an update.
            reference: Optional reference tensor(s), in case of a comparative loss.

        Returns:
            Loss per instance tensor.
        """
        raise NotImplementedError