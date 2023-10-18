def tf_baseline_loss(self, states, internals, reward, update, reference=None):
        """
        Creates the TensorFlow operations for calculating the baseline loss of a batch.

        Args:
            states: Dict of state tensors.
            internals: List of prior internal state tensors.
            reward: Reward tensor.
            update: Boolean tensor indicating whether this call happens during an update.
            reference: Optional reference tensor(s), in case of a comparative loss.

        Returns:
            Loss tensor.
        """
        if self.baseline_mode == 'states':
            loss = self.baseline.loss(
                states=states,
                internals=internals,
                reward=reward,
                update=update,
                reference=reference
            )

        elif self.baseline_mode == 'network':
            loss = self.baseline.loss(
                states=self.network.apply(x=states, internals=internals, update=update),
                internals=internals,
                reward=reward,
                update=update,
                reference=reference
            )

        regularization_loss = self.baseline.regularization_loss()
        if regularization_loss is not None:
            loss += regularization_loss

        return loss