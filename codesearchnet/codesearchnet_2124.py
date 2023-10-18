def tf_loss(self, states, internals, actions, terminal, reward, next_states, next_internals, update, reference=None):
        """
        Creates the TensorFlow operations for calculating the full loss of a batch.

        Args:
            states: Dict of state tensors.
            internals: List of prior internal state tensors.
            actions: Dict of action tensors.
            terminal: Terminal boolean tensor.
            reward: Reward tensor.
            next_states: Dict of successor state tensors.
            next_internals: List of posterior internal state tensors.
            update: Boolean tensor indicating whether this call happens during an update.
            reference: Optional reference tensor(s), in case of a comparative loss.

        Returns:
            Loss tensor.
        """
        # Mean loss per instance
        loss_per_instance = self.fn_loss_per_instance(
            states=states,
            internals=internals,
            actions=actions,
            terminal=terminal,
            reward=reward,
            next_states=next_states,
            next_internals=next_internals,
            update=update,
            reference=reference
        )

        # Returns no-op.
        updated = self.memory.update_batch(loss_per_instance=loss_per_instance)
        with tf.control_dependencies(control_inputs=(updated,)):
            loss = tf.reduce_mean(input_tensor=loss_per_instance, axis=0)

            # Loss without regularization summary.
            if 'losses' in self.summary_labels:
                tf.contrib.summary.scalar(name='loss-without-regularization', tensor=loss)

            # Regularization losses.
            losses = self.fn_regularization_losses(states=states, internals=internals, update=update)
            if len(losses) > 0:
                loss += tf.add_n(inputs=[losses[name] for name in sorted(losses)])
                if 'regularization' in self.summary_labels:
                    for name in sorted(losses):
                        tf.contrib.summary.scalar(name=('regularization/' + name), tensor=losses[name])

            # Total loss summary.
            if 'losses' in self.summary_labels or 'total-loss' in self.summary_labels:
                tf.contrib.summary.scalar(name='total-loss', tensor=loss)

            return loss