def tf_loss(self, states, internals, reward, update, reference=None):
        """
        Creates the TensorFlow operations for calculating the L2 loss between predicted
        state values and actual rewards.

        Args:
            states: Dict of state tensors.
            internals: List of prior internal state tensors.
            reward: Reward tensor.
            update: Boolean tensor indicating whether this call happens during an update.
            reference: Optional reference tensor(s), in case of a comparative loss.

        Returns:
            Loss tensor
        """
        prediction = self.predict(states=states, internals=internals, update=update)
        return tf.nn.l2_loss(t=(prediction - reward))